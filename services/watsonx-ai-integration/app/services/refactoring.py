"""
Code refactoring service using watsonx.ai
"""

import json
import time
import difflib
from typing import Dict, Any, List

from ..models.request import RefactoringRequest
from ..models.response import RefactoredCode
from ..prompts.refactoring import build_refactoring_prompt
from ..utils.logger import get_logger
from .watsonx_client import WatsonxClient

logger = get_logger(__name__)


class RefactoringService:
    """
    Service for AI-powered code refactoring
    Uses watsonx.ai to optimize code while preserving functionality
    """
    
    def __init__(self, watsonx_client: WatsonxClient):
        """
        Initialize refactoring service
        
        Args:
            watsonx_client: Configured watsonx.ai client
        """
        self.client = watsonx_client
        logger.info("RefactoringService initialized")
    
    async def refactor_code(self, request: RefactoringRequest) -> Dict[str, Any]:
        """
        Refactor and optimize code
        
        Args:
            request: Refactoring request
            
        Returns:
            Dictionary containing refactored code and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Refactoring {request.language} code")
            logger.debug(f"Original code length: {len(request.original_code)} chars")
            logger.debug(f"Inefficient patterns: {request.inefficient_patterns}")
            
            # Build prompt
            prompt = build_refactoring_prompt(
                original_code=request.original_code,
                language=request.language.value,
                inefficient_patterns=request.inefficient_patterns,
                target_complexity=request.target_complexity,
                optimization_focus=request.optimization_focus.value
            )
            
            # Select model and temperature
            model_id = self.client.primary_model  # Always use primary for refactoring
            temperature = 0.2  # Low temperature for more deterministic refactoring
            
            logger.debug(f"Using model: {model_id}, temperature: {temperature}")
            
            # Generate refactored code using watsonx.ai
            response = await self.client.generate(
                prompt=prompt,
                model_id=model_id,
                max_tokens=2048,
                temperature=temperature,
                top_p=0.9
            )
            
            # Parse response
            refactored_code = self._parse_refactoring_response(response, request)
            
            # Generate diff
            diff = self._generate_diff(
                request.original_code,
                refactored_code.refactored_code
            )
            refactored_code.diff = diff
            
            processing_time = (time.time() - start_time) * 1000
            logger.info(f"Code refactoring completed in {processing_time:.2f}ms")
            
            return {
                "success": True,
                "refactored_code": refactored_code,
                "processing_time_ms": processing_time,
                "model_used": model_id,
                "confidence_score": self._calculate_confidence(refactored_code)
            }
            
        except Exception as e:
            logger.error(f"Code refactoring failed: {e}", exc_info=True)
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": processing_time
            }
    
    def _parse_refactoring_response(
        self,
        response: Dict[str, Any],
        request: RefactoringRequest
    ) -> RefactoredCode:
        """
        Parse watsonx.ai response into RefactoredCode model
        
        Args:
            response: Raw response from watsonx.ai
            request: Original request
            
        Returns:
            Parsed RefactoredCode object
        """
        try:
            # Extract generated text
            generated_text = response["results"][0]["generated_text"]
            
            # Try to parse as JSON
            try:
                data = json.loads(generated_text)
            except json.JSONDecodeError:
                # If not JSON, extract code from text
                data = self._extract_refactored_code_from_text(
                    generated_text,
                    request.language.value
                )
            
            # Create RefactoredCode object
            return RefactoredCode(
                original_code=request.original_code,
                refactored_code=data.get("refactored_code", generated_text),
                changes_made=data.get("changes_made", []),
                complexity_improvement={
                    "before": data.get("complexity_before", {"time": "Unknown", "space": "Unknown"}),
                    "after": data.get("complexity_after", {"time": "Unknown", "space": "Unknown"})
                },
                explanation=data.get("explanation", "Refactored code (parsing incomplete)"),
                preserved_functionality=request.preserve_functionality
            )
            
        except Exception as e:
            logger.error(f"Failed to parse refactoring response: {e}")
            # Return minimal valid response
            return RefactoredCode(
                original_code=request.original_code,
                refactored_code="# Error parsing refactored code\n# " + str(e),
                changes_made=[],
                complexity_improvement={
                    "before": {"time": "Unknown", "space": "Unknown"},
                    "after": {"time": "Unknown", "space": "Unknown"}
                },
                explanation="Error occurred during refactoring",
                preserved_functionality=False
            )
    
    def _extract_refactored_code_from_text(
        self,
        text: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Extract refactored code from plain text response
        
        Args:
            text: Generated text
            language: Programming language
            
        Returns:
            Dictionary with extracted code and metadata
        """
        # Try to find code blocks
        code_block_markers = [f"```{language}", "```python", "```java", "```cpp", "```"]
        
        refactored_code = text
        for marker in code_block_markers:
            if marker in text:
                parts = text.split(marker)
                if len(parts) >= 2:
                    refactored_code = parts[1].split("```")[0].strip()
                    break
        
        return {
            "refactored_code": refactored_code,
            "changes_made": ["Extracted from text response"],
            "complexity_before": {"time": "Not specified", "space": "Not specified"},
            "complexity_after": {"time": "Not specified", "space": "Not specified"},
            "explanation": "Refactored code (metadata incomplete)"
        }
    
    def _generate_diff(self, original: str, refactored: str) -> str:
        """
        Generate unified diff between original and refactored code
        
        Args:
            original: Original code
            refactored: Refactored code
            
        Returns:
            Unified diff string
        """
        original_lines = original.splitlines(keepends=True)
        refactored_lines = refactored.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            original_lines,
            refactored_lines,
            fromfile='original',
            tofile='refactored',
            lineterm=''
        )
        
        return ''.join(diff)
    
    def _calculate_confidence(self, refactored_code: RefactoredCode) -> float:
        """
        Calculate confidence score for refactored code
        
        Args:
            refactored_code: Refactored code object
            
        Returns:
            Confidence score (0-1)
        """
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on available metadata
        if refactored_code.changes_made:
            confidence += 0.15
        
        if refactored_code.explanation and len(refactored_code.explanation) > 50:
            confidence += 0.15
        
        # Check if complexity improved
        before = refactored_code.complexity_improvement.get("before", {})
        after = refactored_code.complexity_improvement.get("after", {})
        
        if before.get("time") != "Unknown" and after.get("time") != "Unknown":
            confidence += 0.1
            # Check if actually improved
            if self._is_complexity_improved(before.get("time"), after.get("time")):
                confidence += 0.1
        
        # Check code quality
        if len(refactored_code.refactored_code.split('\n')) > 3:
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    def _is_complexity_improved(self, before: str, after: str) -> bool:
        """
        Check if complexity improved
        
        Args:
            before: Original complexity
            after: New complexity
            
        Returns:
            True if improved
        """
        # Simple heuristic: check if O notation improved
        complexity_order = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n²)": 5,
            "O(n^2)": 5,
            "O(2^n)": 6,
            "O(n!)": 7
        }
        
        before_order = complexity_order.get(before, 999)
        after_order = complexity_order.get(after, 999)
        
        return after_order < before_order
    
    async def analyze_refactoring_impact(
        self,
        original: str,
        refactored: str
    ) -> Dict[str, Any]:
        """
        Analyze the impact of refactoring
        
        Args:
            original: Original code
            refactored: Refactored code
            
        Returns:
            Impact analysis
        """
        analysis = {
            "lines_changed": 0,
            "lines_added": 0,
            "lines_removed": 0,
            "similarity_score": 0.0
        }
        
        # Calculate line changes
        original_lines = original.splitlines()
        refactored_lines = refactored.splitlines()
        
        analysis["lines_removed"] = len(original_lines) - len(refactored_lines)
        analysis["lines_added"] = len(refactored_lines) - len(original_lines)
        
        # Calculate similarity
        matcher = difflib.SequenceMatcher(None, original, refactored)
        analysis["similarity_score"] = matcher.ratio()
        
        # Count actual changes
        diff = list(difflib.unified_diff(original_lines, refactored_lines))
        analysis["lines_changed"] = len([line for line in diff if line.startswith('+') or line.startswith('-')])
        
        return analysis

# Made with Bob