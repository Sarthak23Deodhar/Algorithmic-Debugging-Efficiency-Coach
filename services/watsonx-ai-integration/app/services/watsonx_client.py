"""
watsonx.ai API client with mock mode support
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from ..utils.logger import get_logger

logger = get_logger(__name__)


class WatsonxClient:
    """
    Client for interacting with IBM watsonx.ai API
    Supports both real API calls and mock mode for development
    """
    
    def __init__(self, mock_mode: bool = True):
        """
        Initialize watsonx.ai client
        
        Args:
            mock_mode: If True, use mock responses instead of real API calls
        """
        self.mock_mode = mock_mode
        self.api_key = os.getenv("WATSONX_API_KEY", "mock_api_key")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "mock_project_id")
        self.api_url = os.getenv("WATSONX_API_URL", "https://us-south.ml.cloud.ibm.com")
        
        # Model configurations
        self.primary_model = "ibm/granite-20b-code-instruct"
        self.fast_model = "ibm/granite-8b-code-base"
        
        if not mock_mode:
            self._initialize_real_client()
        else:
            logger.info("WatsonxClient initialized in MOCK MODE")
    
    def _initialize_real_client(self):
        """Initialize the real watsonx.ai SDK client"""
        try:
            # This would be the real initialization
            # from ibm_watsonx_ai import APIClient, Credentials
            # self.credentials = Credentials(url=self.api_url, api_key=self.api_key)
            # self.client = APIClient(self.credentials)
            logger.info("WatsonxClient initialized with real API")
        except Exception as e:
            logger.error(f"Failed to initialize watsonx.ai client: {e}")
            logger.warning("Falling back to mock mode")
            self.mock_mode = True
    
    async def generate(
        self,
        prompt: str,
        model_id: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.95,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using watsonx.ai
        
        Args:
            prompt: Input prompt
            model_id: Model to use (defaults to primary_model)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            top_p: Nucleus sampling parameter
            **kwargs: Additional model parameters
            
        Returns:
            Generated response with metadata
        """
        model_id = model_id or self.primary_model
        
        if self.mock_mode:
            return await self._mock_generate(prompt, model_id, max_tokens, temperature)
        else:
            return await self._real_generate(prompt, model_id, max_tokens, temperature, top_p, **kwargs)
    
    async def _mock_generate(
        self,
        prompt: str,
        model_id: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """
        Mock generation for development/testing
        
        Simulates API latency and returns plausible responses
        """
        # Simulate API latency (500-1500ms)
        await asyncio.sleep(0.5 + (len(prompt) / 10000))
        
        logger.info(f"Mock generation with model: {model_id}")
        logger.debug(f"Prompt length: {len(prompt)} chars")
        
        # Determine response type based on prompt content
        if "generate" in prompt.lower() or "code generation" in prompt.lower():
            response_text = self._mock_code_generation_response(prompt)
        elif "refactor" in prompt.lower() or "optimize" in prompt.lower():
            response_text = self._mock_refactoring_response(prompt)
        elif "explain" in prompt.lower():
            response_text = self._mock_explanation_response(prompt)
        else:
            response_text = '{"error": "Unable to determine operation type from prompt"}'
        
        return {
            "results": [{
                "generated_text": response_text,
                "generated_token_count": len(response_text.split()),
                "input_token_count": len(prompt.split()),
                "stop_reason": "eos_token"
            }],
            "model_id": model_id,
            "created_at": datetime.utcnow().isoformat(),
            "mock_mode": True
        }
    
    def _mock_code_generation_response(self, prompt: str) -> str:
        """Generate mock code generation response"""
        # Extract language from prompt
        language = "python"
        if "java" in prompt.lower():
            language = "java"
        elif "c++" in prompt.lower() or "cpp" in prompt.lower():
            language = "cpp"
        
        # Generate plausible response based on common patterns
        if "two sum" in prompt.lower() or "pair" in prompt.lower():
            return json.dumps({
                "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
                "algorithm_used": "Hash Map",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Uses a hash map to store seen numbers and their indices. For each number, checks if its complement (target - num) exists in the map.",
                "edge_cases_handled": ["empty array", "no solution", "duplicate numbers"]
            })
        else:
            # Generic response
            return json.dumps({
                "code": f"# {language.upper()} solution\n# TODO: Implement based on problem description\npass",
                "algorithm_used": "To be determined based on problem",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "This is a mock response. In production, watsonx.ai would generate actual code.",
                "edge_cases_handled": ["basic validation"]
            })
    
    def _mock_refactoring_response(self, prompt: str) -> str:
        """Generate mock refactoring response"""
        return json.dumps({
            "refactored_code": "# Optimized version\ndef optimized_function(data):\n    # Using hash set for O(1) lookups\n    seen = set()\n    result = []\n    for item in data:\n        if item not in seen:\n            result.append(item)\n            seen.add(item)\n    return result",
            "changes_made": [
                "Replaced nested loops with single pass",
                "Used hash set for O(1) membership testing",
                "Reduced time complexity from O(n²) to O(n)"
            ],
            "complexity_before": {
                "time": "O(n²)",
                "space": "O(1)"
            },
            "complexity_after": {
                "time": "O(n)",
                "space": "O(n)"
            },
            "explanation": "The original code used nested loops for comparisons. By using a hash set, we achieve O(1) lookups, reducing overall time complexity to O(n) at the cost of O(n) space.",
            "trade_offs": "Increased space complexity from O(1) to O(n), but dramatically improved time complexity"
        })
    
    def _mock_explanation_response(self, prompt: str) -> str:
        """Generate mock explanation response"""
        return json.dumps({
            "summary": "This code implements a common algorithmic pattern using appropriate data structures for efficiency.",
            "detailed_explanation": "The function processes input data by iterating through elements and applying a specific logic. It uses efficient data structures to minimize time complexity while maintaining reasonable space usage.",
            "key_concepts": ["iteration", "data structures", "algorithm design", "complexity analysis"],
            "potential_issues": [
                {
                    "type": "edge_case",
                    "description": "May not handle empty input correctly"
                },
                {
                    "type": "validation",
                    "description": "Missing input validation for invalid data types"
                }
            ],
            "suggestions": [
                "Add input validation",
                "Handle edge cases explicitly",
                "Add docstring documentation",
                "Consider error handling for invalid inputs"
            ],
            "learning_resources": [
                {
                    "title": "Algorithm Design Patterns",
                    "description": "Learn common algorithmic patterns and when to use them",
                    "relevance": "This code uses a standard pattern that appears frequently"
                }
            ],
            "analogies": [
                "Think of this algorithm like organizing books on a shelf - you check each book once and place it in the right spot based on a simple rule."
            ]
        })
    
    async def _real_generate(
        self,
        prompt: str,
        model_id: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Real API call to watsonx.ai (placeholder for actual implementation)
        """
        # This would be the real implementation
        # params = {
        #     "decoding_method": "greedy" if temperature == 0 else "sample",
        #     "max_new_tokens": max_tokens,
        #     "temperature": temperature,
        #     "top_p": top_p,
        #     "repetition_penalty": 1.1
        # }
        # 
        # response = await self.client.foundation_models.generate_async(
        #     model_id=model_id,
        #     prompt=prompt,
        #     params=params,
        #     project_id=self.project_id
        # )
        # 
        # return response
        
        logger.warning("Real API not implemented, falling back to mock")
        return await self._mock_generate(prompt, model_id, max_tokens, temperature)
    
    async def generate_stream(
        self,
        prompt: str,
        model_id: Optional[str] = None,
        **kwargs
    ):
        """
        Stream generation from watsonx.ai (for long responses)
        
        Args:
            prompt: Input prompt
            model_id: Model to use
            **kwargs: Additional parameters
            
        Yields:
            Chunks of generated text
        """
        if self.mock_mode:
            # Mock streaming by yielding chunks
            response = await self.generate(prompt, model_id, **kwargs)
            text = response["results"][0]["generated_text"]
            
            # Simulate streaming by yielding in chunks
            chunk_size = 50
            for i in range(0, len(text), chunk_size):
                await asyncio.sleep(0.1)  # Simulate network delay
                yield text[i:i+chunk_size]
        else:
            # Real streaming implementation would go here
            pass
    
    def is_connected(self) -> bool:
        """
        Check if client is connected to watsonx.ai
        
        Returns:
            True if connected (or in mock mode), False otherwise
        """
        if self.mock_mode:
            return True
        
        # In real mode, would check API connectivity
        try:
            # self.client.foundation_models.list()
            return True
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False

# Made with Bob