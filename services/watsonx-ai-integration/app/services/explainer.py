"""
Code explanation service using watsonx.ai
"""

import json
import time
from typing import Dict, Any, Optional

from ..models.request import ExplanationRequest
from ..models.response import CodeExplanation
from ..prompts.explanation import build_explanation_prompt
from ..utils.logger import get_logger
from .watsonx_client import WatsonxClient

logger = get_logger(__name__)


class ExplainerService:
    """
    Service for AI-powered code explanation
    Uses watsonx.ai to generate educational explanations of code
    """
    
    def __init__(self, watsonx_client: WatsonxClient):
        """
        Initialize explainer service
        
        Args:
            watsonx_client: Configured watsonx.ai client
        """
        self.client = watsonx_client
        logger.info("ExplainerService initialized")
    
    async def explain_code(self, request: ExplanationRequest) -> Dict[str, Any]:
        """
        Generate comprehensive code explanation
        
        Args:
            request: Explanation request
            
        Returns:
            Dictionary containing explanation and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Explaining {request.language} code")
            logger.debug(f"Code length: {len(request.code)} chars")
            logger.debug(f"Explanation level: {request.explanation_level}")
            logger.debug(f"Focus areas: {request.focus_areas}")
            
            # Build prompt
            prompt = build_explanation_prompt(
                code=request.code,
                language=request.language.value,
                explanation_level=request.explanation_level,
                focus_areas=request.focus_areas,
                bug_report=request.bug_report,
                complexity_analysis=request.complexity_analysis,
                include_analogies=request.include_analogies
            )
            
            # Select model based on explanation complexity
            model_id = self._select_model(request)
            temperature = self._select_temperature(request.explanation_level)
            
            logger.debug(f"Using model: {model_id}, temperature: {temperature}")
            
            # Generate explanation using watsonx.ai
            response = await self.client.generate(
                prompt=prompt,
                model_id=model_id,
                max_tokens=1024,  # Explanations typically shorter than code
                temperature=temperature,
                top_p=0.95
            )
            
            # Parse response
            explanation = self._parse_explanation_response(response, request)
            
            processing_time = (time.time() - start_time) * 1000
            logger.info(f"Code explanation completed in {processing_time:.2f}ms")
            
            return {
                "success": True,
                "explanation": explanation,
                "processing_time_ms": processing_time,
                "model_used": model_id,
                "confidence_score": self._calculate_confidence(explanation)
            }
            
        except Exception as e:
            logger.error(f"Code explanation failed: {e}", exc_info=True)
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": processing_time
            }
    
    def _select_model(self, request: ExplanationRequest) -> str:
        """
        Select appropriate model based on explanation complexity
        
        Args:
            request: Explanation request
            
        Returns:
            Model ID to use
        """
        # Use fast model for simple explanations, primary for complex
        has_context = request.bug_report is not None or request.complexity_analysis is not None
        is_advanced = request.explanation_level == "advanced"
        has_focus = request.focus_areas and len(request.focus_areas) > 0
        
        if has_context or is_advanced or has_focus:
            return self.client.primary_model
        else:
            return self.client.fast_model
    
    def _select_temperature(self, explanation_level: str) -> float:
        """
        Select temperature based on explanation level
        
        Args:
            explanation_level: Target audience level
            
        Returns:
            Temperature value (0-1)
        """
        # Higher temperature for beginner (more creative/analogies)
        # Lower temperature for advanced (more technical/precise)
        temperature_map = {
            "beginner": 0.8,
            "intermediate": 0.6,
            "advanced": 0.4
        }
        return temperature_map.get(explanation_level, 0.6)
    
    def _parse_explanation_response(
        self,
        response: Dict[str, Any],
        request: ExplanationRequest
    ) -> CodeExplanation:
        """
        Parse watsonx.ai response into CodeExplanation model
        
        Args:
            response: Raw response from watsonx.ai
            request: Original request
            
        Returns:
            Parsed CodeExplanation object
        """
        try:
            # Extract generated text
            generated_text = response["results"][0]["generated_text"]
            
            # Try to parse as JSON
            try:
                data = json.loads(generated_text)
            except json.JSONDecodeError:
                # If not JSON, create structured explanation from text
                data = self._extract_explanation_from_text(generated_text)
            
            # Create CodeExplanation object
            return CodeExplanation(
                summary=data.get("summary", "Code explanation generated"),
                detailed_explanation=data.get("detailed_explanation", generated_text),
                key_concepts=data.get("key_concepts", []),
                potential_issues=data.get("potential_issues", []),
                suggestions=data.get("suggestions", []),
                learning_resources=data.get("learning_resources", []),
                analogies=data.get("analogies", []) if request.include_analogies else []
            )
            
        except Exception as e:
            logger.error(f"Failed to parse explanation response: {e}")
            # Return minimal valid response
            return CodeExplanation(
                summary="Error generating explanation",
                detailed_explanation=f"An error occurred: {str(e)}",
                key_concepts=[],
                potential_issues=[],
                suggestions=[],
                learning_resources=[],
                analogies=[]
            )
    
    def _extract_explanation_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract structured explanation from plain text
        
        Args:
            text: Generated text
            
        Returns:
            Dictionary with explanation components
        """
        # Simple extraction - split by common section headers
        sections = {
            "summary": "",
            "detailed_explanation": text,
            "key_concepts": [],
            "potential_issues": [],
            "suggestions": [],
            "learning_resources": [],
            "analogies": []
        }
        
        # Try to extract summary (first paragraph)
        paragraphs = text.split('\n\n')
        if paragraphs:
            sections["summary"] = paragraphs[0][:200]  # First 200 chars
        
        # Extract key concepts (look for bullet points or numbered lists)
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith(('-', '*', '•')) or line.strip()[0:2].isdigit():
                concept = line.strip().lstrip('-*•0123456789. ')
                if concept and len(concept) > 5:
                    sections["key_concepts"].append(concept)
        
        return sections
    
    def _calculate_confidence(self, explanation: CodeExplanation) -> float:
        """
        Calculate confidence score for explanation
        
        Args:
            explanation: Code explanation object
            
        Returns:
            Confidence score (0-1)
        """
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on completeness
        if explanation.summary and len(explanation.summary) > 20:
            confidence += 0.1
        
        if explanation.detailed_explanation and len(explanation.detailed_explanation) > 100:
            confidence += 0.15
        
        if explanation.key_concepts and len(explanation.key_concepts) > 0:
            confidence += 0.1
        
        if explanation.suggestions and len(explanation.suggestions) > 0:
            confidence += 0.1
        
        if explanation.analogies and len(explanation.analogies) > 0:
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    async def explain_bug(
        self,
        code: str,
        language: str,
        bug_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate explanation specifically focused on bugs
        
        Args:
            code: Code with bugs
            language: Programming language
            bug_report: Bug report from debugging engine
            
        Returns:
            Bug-focused explanation
        """
        request = ExplanationRequest(
            code=code,
            language=language,
            bug_report=bug_report,
            explanation_level="beginner",
            focus_areas=["bugs"],
            include_analogies=True
        )
        
        return await self.explain_code(request)
    
    async def explain_inefficiency(
        self,
        code: str,
        language: str,
        complexity_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate explanation specifically focused on inefficiencies
        
        Args:
            code: Inefficient code
            language: Programming language
            complexity_analysis: Complexity analysis from efficiency analyzer
            
        Returns:
            Inefficiency-focused explanation
        """
        request = ExplanationRequest(
            code=code,
            language=language,
            complexity_analysis=complexity_analysis,
            explanation_level="intermediate",
            focus_areas=["inefficiencies", "algorithm"],
            include_analogies=True
        )
        
        return await self.explain_code(request)
    
    def generate_learning_path(
        self,
        key_concepts: list,
        current_level: str = "beginner"
    ) -> list:
        """
        Generate a learning path based on identified concepts
        
        Args:
            key_concepts: List of concepts from explanation
            current_level: Current skill level
            
        Returns:
            Ordered list of learning resources
        """
        # Map concepts to learning resources
        concept_resources = {
            "recursion": {
                "title": "Understanding Recursion",
                "topics": ["base case", "recursive case", "call stack"],
                "difficulty": "intermediate"
            },
            "dynamic programming": {
                "title": "Dynamic Programming Fundamentals",
                "topics": ["memoization", "tabulation", "optimal substructure"],
                "difficulty": "advanced"
            },
            "hash map": {
                "title": "Hash Tables and Maps",
                "topics": ["hashing", "collision resolution", "time complexity"],
                "difficulty": "beginner"
            },
            "two pointers": {
                "title": "Two Pointer Technique",
                "topics": ["array traversal", "optimization patterns"],
                "difficulty": "intermediate"
            }
        }
        
        learning_path = []
        for concept in key_concepts:
            concept_lower = concept.lower()
            for key, resource in concept_resources.items():
                if key in concept_lower:
                    learning_path.append(resource)
                    break
        
        # Sort by difficulty based on current level
        difficulty_order = {"beginner": 1, "intermediate": 2, "advanced": 3}
        current_order = difficulty_order.get(current_level, 1)
        
        learning_path.sort(key=lambda x: abs(difficulty_order.get(x["difficulty"], 2) - current_order))
        
        return learning_path

# Made with Bob