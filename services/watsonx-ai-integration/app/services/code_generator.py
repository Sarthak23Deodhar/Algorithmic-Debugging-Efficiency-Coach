"""
Code generation service using watsonx.ai
"""

import json
import time
from typing import Dict, Any

from ..models.request import CodeGenerationRequest
from ..models.response import GeneratedCode
from ..prompts.code_generation import build_generation_prompt
from ..utils.logger import get_logger
from .watsonx_client import WatsonxClient

logger = get_logger(__name__)


class CodeGeneratorService:
    """
    Service for AI-powered code generation
    Uses watsonx.ai to generate optimized code from problem descriptions
    """
    
    def __init__(self, watsonx_client: WatsonxClient):
        """
        Initialize code generator service
        
        Args:
            watsonx_client: Configured watsonx.ai client
        """
        self.client = watsonx_client
        logger.info("CodeGeneratorService initialized")
    
    async def generate_code(self, request: CodeGenerationRequest) -> Dict[str, Any]:
        """
        Generate optimized code from problem description
        
        Args:
            request: Code generation request
            
        Returns:
            Dictionary containing generated code and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Generating {request.language} code for problem")
            logger.debug(f"Problem: {request.problem_description[:100]}...")
            
            # Build prompt
            prompt = build_generation_prompt(
                problem_description=request.problem_description,
                language=request.language.value,
                constraints=request.constraints,
                optimization_target=request.optimization_target.value,
                examples=request.examples
            )
            
            # Determine model and parameters based on complexity
            model_id = self._select_model(request)
            temperature = self._select_temperature(request.optimization_target.value)
            
            logger.debug(f"Using model: {model_id}, temperature: {temperature}")
            
            # Generate code using watsonx.ai
            response = await self.client.generate(
                prompt=prompt,
                model_id=model_id,
                max_tokens=2048,
                temperature=temperature,
                top_p=0.95
            )
            
            # Parse response
            generated_code = self._parse_generation_response(response, request)
            
            processing_time = (time.time() - start_time) * 1000
            logger.info(f"Code generation completed in {processing_time:.2f}ms")
            
            return {
                "success": True,
                "generated_code": generated_code,
                "processing_time_ms": processing_time,
                "model_used": model_id,
                "confidence_score": self._calculate_confidence(generated_code)
            }
            
        except Exception as e:
            logger.error(f"Code generation failed: {e}", exc_info=True)
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": processing_time
            }
    
    def _select_model(self, request: CodeGenerationRequest) -> str:
        """
        Select appropriate model based on request complexity
        
        Args:
            request: Code generation request
            
        Returns:
            Model ID to use
        """
        # Use primary model for complex tasks, fast model for simple ones
        problem_length = len(request.problem_description)
        has_constraints = request.constraints is not None
        has_examples = request.examples is not None and len(request.examples) > 0
        
        # Complex task indicators
        if problem_length > 500 or has_constraints or has_examples:
            return self.client.primary_model
        else:
            return self.client.fast_model
    
    def _select_temperature(self, optimization_target: str) -> float:
        """
        Select temperature based on optimization target
        
        Args:
            optimization_target: What to optimize for
            
        Returns:
            Temperature value (0-1)
        """
        # Lower temperature for time/space optimization (more deterministic)
        # Higher temperature for readability (more creative)
        temperature_map = {
            "time_complexity": 0.3,
            "space_complexity": 0.3,
            "balanced": 0.5,
            "readability": 0.7
        }
        return temperature_map.get(optimization_target, 0.5)
    
    def _parse_generation_response(
        self,
        response: Dict[str, Any],
        request: CodeGenerationRequest
    ) -> GeneratedCode:
        """
        Parse watsonx.ai response into GeneratedCode model
        
        Args:
            response: Raw response from watsonx.ai
            request: Original request
            
        Returns:
            Parsed GeneratedCode object
        """
        try:
            # Extract generated text
            generated_text = response["results"][0]["generated_text"]
            
            # Try to parse as JSON
            try:
                data = json.loads(generated_text)
            except json.JSONDecodeError:
                # If not JSON, extract code from markdown or plain text
                data = self._extract_code_from_text(generated_text, request.language.value)
            
            # Create GeneratedCode object
            return GeneratedCode(
                code=data.get("code", generated_text),
                language=request.language.value,
                algorithm_used=data.get("algorithm_used"),
                complexity_analysis={
                    "time": data.get("time_complexity", "Not specified"),
                    "space": data.get("space_complexity", "Not specified")
                },
                explanation=data.get("explanation"),
                test_cases=data.get("test_cases", [])
            )
            
        except Exception as e:
            logger.error(f"Failed to parse generation response: {e}")
            # Return minimal valid response
            return GeneratedCode(
                code="# Error parsing generated code\n# " + str(e),
                language=request.language.value,
                complexity_analysis={"time": "Unknown", "space": "Unknown"}
            )
    
    def _extract_code_from_text(self, text: str, language: str) -> Dict[str, Any]:
        """
        Extract code from plain text or markdown response
        
        Args:
            text: Generated text
            language: Programming language
            
        Returns:
            Dictionary with extracted code and metadata
        """
        # Try to find code blocks
        code_block_markers = [f"```{language}", "```python", "```java", "```cpp", "```"]
        
        code = text
        for marker in code_block_markers:
            if marker in text:
                parts = text.split(marker)
                if len(parts) >= 2:
                    code = parts[1].split("```")[0].strip()
                    break
        
        return {
            "code": code,
            "algorithm_used": "Not specified",
            "time_complexity": "Not specified",
            "space_complexity": "Not specified",
            "explanation": "Generated code (parsing incomplete)"
        }
    
    def _calculate_confidence(self, generated_code: GeneratedCode) -> float:
        """
        Calculate confidence score for generated code
        
        Args:
            generated_code: Generated code object
            
        Returns:
            Confidence score (0-1)
        """
        confidence = 0.5  # Base confidence
        
        # Increase confidence if we have good metadata
        if generated_code.algorithm_used:
            confidence += 0.15
        
        if generated_code.explanation:
            confidence += 0.15
        
        if generated_code.complexity_analysis.get("time") != "Not specified":
            confidence += 0.1
        
        if generated_code.test_cases:
            confidence += 0.1
        
        # Check code quality indicators
        code_lines = generated_code.code.split('\n')
        if len(code_lines) > 3:  # Has substantial code
            confidence += 0.05
        
        if any(keyword in generated_code.code for keyword in ['def ', 'class ', 'function ', 'public ']):
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    async def validate_generated_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Validate generated code for syntax errors
        
        Args:
            code: Generated code
            language: Programming language
            
        Returns:
            Validation results
        """
        # Basic syntax validation
        # In production, this would use language-specific parsers
        
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check for common issues
        if not code.strip():
            validation_result["is_valid"] = False
            validation_result["errors"].append("Generated code is empty")
        
        # Language-specific checks
        if language == "python":
            # Check for basic Python syntax
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError as e:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Syntax error: {e}")
        
        return validation_result

# Made with Bob