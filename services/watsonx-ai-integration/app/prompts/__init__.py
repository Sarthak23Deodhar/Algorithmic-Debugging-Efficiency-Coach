"""
Prompt templates package for watsonx.ai Integration service
"""

from .code_generation import build_generation_prompt
from .refactoring import build_refactoring_prompt
from .explanation import build_explanation_prompt

__all__ = [
    "build_generation_prompt",
    "build_refactoring_prompt",
    "build_explanation_prompt"
]

# Made with Bob