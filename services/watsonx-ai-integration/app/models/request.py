"""
Request models for watsonx.ai Integration service
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


class ProgrammingLanguage(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    CPP = "cpp"
    JAVA = "java"


class OperationType(str, Enum):
    """Types of AI operations"""
    GENERATE = "generate"
    REFACTOR = "refactor"
    EXPLAIN = "explain"


class OptimizationTarget(str, Enum):
    """Optimization targets for code generation"""
    TIME_COMPLEXITY = "time_complexity"
    SPACE_COMPLEXITY = "space_complexity"
    READABILITY = "readability"
    BALANCED = "balanced"


class CodeGenerationRequest(BaseModel):
    """
    Request model for AI-powered code generation
    
    Attributes:
        problem_description: Natural language description of the problem
        language: Target programming language
        constraints: Optional constraints (e.g., "must use O(n) time")
        optimization_target: What to optimize for
        include_comments: Whether to include explanatory comments
        examples: Optional input/output examples
    """
    problem_description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Natural language description of the problem to solve"
    )
    
    language: ProgrammingLanguage = Field(
        ...,
        description="Target programming language for generated code"
    )
    
    constraints: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional constraints (e.g., time/space complexity requirements)"
    )
    
    optimization_target: OptimizationTarget = Field(
        default=OptimizationTarget.BALANCED,
        description="What aspect to optimize for"
    )
    
    include_comments: bool = Field(
        default=True,
        description="Whether to include explanatory comments in generated code"
    )
    
    examples: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Optional input/output examples to guide generation"
    )
    
    webhook_url: Optional[str] = Field(
        None,
        description="Optional webhook URL for async result delivery"
    )
    
    @validator('problem_description')
    def validate_problem_description(cls, v):
        """Ensure problem description is meaningful"""
        if not v.strip():
            raise ValueError("Problem description cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "problem_description": "Find all pairs in an array that sum to a target value",
                "language": "python",
                "constraints": "Must be O(n) time complexity",
                "optimization_target": "time_complexity",
                "include_comments": True,
                "examples": [
                    {"input": "[2, 7, 11, 15], target=9", "output": "[(0, 1)]"}
                ]
            }
        }


class RefactoringRequest(BaseModel):
    """
    Request model for AI-powered code refactoring
    
    Attributes:
        original_code: Code to be refactored
        language: Programming language of the code
        inefficient_patterns: List of detected inefficient patterns
        target_complexity: Target time/space complexity
        preserve_functionality: Whether to strictly preserve functionality
        optimization_focus: What to focus on during refactoring
    """
    original_code: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Original code to be refactored"
    )
    
    language: ProgrammingLanguage = Field(
        ...,
        description="Programming language of the code"
    )
    
    inefficient_patterns: List[str] = Field(
        default_factory=list,
        description="List of detected inefficient patterns (e.g., 'nested_loops', 'redundant_computation')"
    )
    
    target_complexity: Optional[str] = Field(
        None,
        description="Target complexity (e.g., 'O(n log n)', 'O(1) space')"
    )
    
    preserve_functionality: bool = Field(
        default=True,
        description="Whether to strictly preserve original functionality"
    )
    
    optimization_focus: OptimizationTarget = Field(
        default=OptimizationTarget.BALANCED,
        description="Primary optimization focus"
    )
    
    include_explanation: bool = Field(
        default=True,
        description="Whether to include explanation of changes"
    )
    
    webhook_url: Optional[str] = Field(
        None,
        description="Optional webhook URL for async result delivery"
    )
    
    @validator('original_code')
    def validate_code(cls, v):
        """Ensure code is not empty"""
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_code": "def find_duplicates(arr):\n    duplicates = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j]:\n                duplicates.append(arr[i])\n    return duplicates",
                "language": "python",
                "inefficient_patterns": ["nested_loops", "O(n^2)_time"],
                "target_complexity": "O(n) time",
                "preserve_functionality": True,
                "optimization_focus": "time_complexity",
                "include_explanation": True
            }
        }


class ExplanationRequest(BaseModel):
    """
    Request model for AI-powered code explanation
    
    Attributes:
        code: Code to explain
        language: Programming language
        bug_report: Optional bug report from debugging engine
        complexity_analysis: Optional complexity analysis from efficiency analyzer
        explanation_level: Target audience level (beginner, intermediate, advanced)
        focus_areas: Specific areas to focus explanation on
    """
    code: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Code to explain"
    )
    
    language: ProgrammingLanguage = Field(
        ...,
        description="Programming language of the code"
    )
    
    bug_report: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional bug report from debugging engine"
    )
    
    complexity_analysis: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional complexity analysis from efficiency analyzer"
    )
    
    explanation_level: str = Field(
        default="beginner",
        description="Target audience level: beginner, intermediate, advanced"
    )
    
    focus_areas: List[str] = Field(
        default_factory=list,
        description="Specific areas to focus on (e.g., 'bugs', 'inefficiencies', 'algorithm')"
    )
    
    include_analogies: bool = Field(
        default=True,
        description="Whether to include visual analogies and examples"
    )
    
    webhook_url: Optional[str] = Field(
        None,
        description="Optional webhook URL for async result delivery"
    )
    
    @validator('code')
    def validate_code(cls, v):
        """Ensure code is not empty"""
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v
    
    @validator('explanation_level')
    def validate_level(cls, v):
        """Validate explanation level"""
        valid_levels = ['beginner', 'intermediate', 'advanced']
        if v.lower() not in valid_levels:
            raise ValueError(f"Explanation level must be one of: {', '.join(valid_levels)}")
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                "language": "python",
                "bug_report": {
                    "has_errors": False,
                    "logic_errors": [
                        {"type": "missing_validation", "message": "No check for negative numbers"}
                    ]
                },
                "complexity_analysis": {
                    "time_complexity": "O(n)",
                    "space_complexity": "O(n)"
                },
                "explanation_level": "beginner",
                "focus_areas": ["algorithm", "recursion"],
                "include_analogies": True
            }
        }

# Made with Bob