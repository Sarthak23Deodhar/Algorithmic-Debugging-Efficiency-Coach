"""
Request models for the Debugging Engine API
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator


class ProgrammingLanguage(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    CPP = "cpp"
    JAVA = "java"


class CodeSubmission(BaseModel):
    """
    Model for code submission requests
    
    Attributes:
        language: Programming language of the submitted code
        code: Source code to analyze
        context: Optional context or description of what the code should do
    """
    language: ProgrammingLanguage = Field(
        ...,
        description="Programming language of the code"
    )
    code: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Source code to analyze"
    )
    context: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional context about the code's purpose"
    )
    
    @validator('code')
    def validate_code_not_empty(cls, v):
        """Ensure code is not just whitespace"""
        if not v.strip():
            raise ValueError("Code cannot be empty or only whitespace")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "language": "python",
                "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                "context": "Calculate factorial of a number"
            }
        }

# Made with Bob
