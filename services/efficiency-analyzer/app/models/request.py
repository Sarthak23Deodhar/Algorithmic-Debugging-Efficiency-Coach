"""
Request models for Efficiency Analyzer service
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ProgrammingLanguage(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    CPP = "cpp"
    JAVA = "java"


class CodeAnalysisRequest(BaseModel):
    """Request model for code efficiency analysis"""
    
    language: ProgrammingLanguage = Field(
        ...,
        description="Programming language of the code"
    )
    
    code: str = Field(
        ...,
        min_length=1,
        description="Source code to analyze for efficiency"
    )
    
    context: Optional[str] = Field(
        None,
        description="Additional context about the code (e.g., expected input size, constraints)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "language": "python",
                "code": "def find_duplicates(arr):\n    duplicates = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j]:\n                duplicates.append(arr[i])\n    return duplicates",
                "context": "Array size can be up to 10000 elements"
            }
        }

# Made with Bob
