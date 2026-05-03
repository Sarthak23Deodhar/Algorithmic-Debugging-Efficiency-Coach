"""
Response models for watsonx.ai Integration service
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Status of AI processing jobs"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class GeneratedCode(BaseModel):
    """
    Model for generated code output
    
    Attributes:
        code: The generated code
        language: Programming language
        algorithm_used: Algorithm/pattern used
        complexity_analysis: Time and space complexity
        explanation: How the code works
        test_cases: Suggested test cases
    """
    code: str = Field(..., description="Generated code")
    language: str = Field(..., description="Programming language")
    algorithm_used: Optional[str] = Field(None, description="Algorithm or pattern used")
    complexity_analysis: Dict[str, str] = Field(
        default_factory=dict,
        description="Time and space complexity analysis"
    )
    explanation: Optional[str] = Field(None, description="Explanation of the approach")
    test_cases: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Suggested test cases"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
                "language": "python",
                "algorithm_used": "Hash Map (Two Pointers variant)",
                "complexity_analysis": {
                    "time": "O(n)",
                    "space": "O(n)"
                },
                "explanation": "Uses a hash map to store seen numbers and their indices. For each number, checks if its complement exists in the map.",
                "test_cases": [
                    {"input": "[2, 7, 11, 15], 9", "output": "[0, 1]"},
                    {"input": "[3, 2, 4], 6", "output": "[1, 2]"}
                ]
            }
        }


class RefactoredCode(BaseModel):
    """
    Model for refactored code output
    
    Attributes:
        original_code: The original code
        refactored_code: The optimized code
        changes_made: List of changes applied
        complexity_improvement: Before/after complexity comparison
        diff: Unified diff showing changes
        explanation: Explanation of each optimization
    """
    original_code: str = Field(..., description="Original code")
    refactored_code: str = Field(..., description="Refactored/optimized code")
    changes_made: List[str] = Field(
        default_factory=list,
        description="List of changes applied"
    )
    complexity_improvement: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description="Before and after complexity comparison"
    )
    diff: Optional[str] = Field(None, description="Unified diff of changes")
    explanation: str = Field(..., description="Detailed explanation of optimizations")
    preserved_functionality: bool = Field(
        default=True,
        description="Whether functionality was preserved"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_code": "def find_duplicates(arr):\n    duplicates = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j]:\n                duplicates.append(arr[i])\n    return duplicates",
                "refactored_code": "def find_duplicates(arr):\n    seen = set()\n    duplicates = set()\n    for num in arr:\n        if num in seen:\n            duplicates.add(num)\n        seen.add(num)\n    return list(duplicates)",
                "changes_made": [
                    "Replaced nested loops with single pass",
                    "Used hash set for O(1) lookups",
                    "Eliminated redundant comparisons"
                ],
                "complexity_improvement": {
                    "before": {"time": "O(n²)", "space": "O(k)"},
                    "after": {"time": "O(n)", "space": "O(n)"}
                },
                "explanation": "Replaced O(n²) nested loop approach with O(n) hash set approach. Trades space for time efficiency.",
                "preserved_functionality": True
            }
        }


class CodeExplanation(BaseModel):
    """
    Model for code explanation output
    
    Attributes:
        summary: High-level summary
        detailed_explanation: Detailed line-by-line or section explanation
        key_concepts: Important concepts used
        potential_issues: Identified issues or concerns
        suggestions: Improvement suggestions
        learning_resources: Related learning materials
        analogies: Visual analogies to aid understanding
    """
    summary: str = Field(..., description="High-level summary of the code")
    detailed_explanation: str = Field(..., description="Detailed explanation")
    key_concepts: List[str] = Field(
        default_factory=list,
        description="Key programming concepts used"
    )
    potential_issues: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Potential issues or bugs identified"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Improvement suggestions"
    )
    learning_resources: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Related learning materials and references"
    )
    analogies: List[str] = Field(
        default_factory=list,
        description="Visual analogies to aid understanding"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "A recursive factorial function that calculates n! by multiplying n with factorial(n-1)",
                "detailed_explanation": "This function uses recursion to calculate factorial. Base case: when n=0, return 1. Recursive case: multiply n by factorial(n-1). Each call reduces n until reaching base case.",
                "key_concepts": ["recursion", "base case", "call stack"],
                "potential_issues": [
                    {"type": "missing_validation", "description": "No check for negative numbers"},
                    {"type": "stack_overflow", "description": "Large n values may cause stack overflow"}
                ],
                "suggestions": [
                    "Add input validation for negative numbers",
                    "Consider iterative approach for large values",
                    "Add memoization for repeated calls"
                ],
                "learning_resources": [
                    {"title": "Understanding Recursion", "url": "https://example.com/recursion"},
                    {"title": "Factorial Algorithms", "url": "https://example.com/factorial"}
                ],
                "analogies": [
                    "Like Russian nesting dolls - each doll contains a smaller version until you reach the smallest one"
                ]
            }
        }


class AIResponse(BaseModel):
    """
    Main response model for all AI operations
    
    Attributes:
        job_id: Unique identifier for this job
        status: Current status of the job
        operation_type: Type of operation (generate, refactor, explain)
        generated_code: Generated code (for generate operations)
        refactored_code: Refactored code (for refactor operations)
        explanation: Code explanation (for explain operations)
        confidence_score: AI confidence in the result (0-1)
        processing_time_ms: Time taken to process
        model_used: watsonx.ai model used
        error_message: Error message if failed
        created_at: Timestamp when job was created
        completed_at: Timestamp when job completed
    """
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    operation_type: str = Field(..., description="Type of operation performed")
    
    # Operation-specific results
    generated_code: Optional[GeneratedCode] = Field(
        None,
        description="Generated code result (for generate operations)"
    )
    refactored_code: Optional[RefactoredCode] = Field(
        None,
        description="Refactored code result (for refactor operations)"
    )
    explanation: Optional[CodeExplanation] = Field(
        None,
        description="Code explanation result (for explain operations)"
    )
    
    # Metadata
    confidence_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="AI confidence score (0-1)"
    )
    processing_time_ms: Optional[float] = Field(
        None,
        description="Processing time in milliseconds"
    )
    model_used: Optional[str] = Field(
        None,
        description="watsonx.ai model used for processing"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if job failed"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Job creation timestamp"
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="Job completion timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "job_abc123xyz",
                "status": "completed",
                "operation_type": "generate",
                "generated_code": {
                    "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
                    "language": "python",
                    "algorithm_used": "Hash Map",
                    "complexity_analysis": {"time": "O(n)", "space": "O(n)"},
                    "explanation": "Uses hash map for O(n) solution"
                },
                "confidence_score": 0.95,
                "processing_time_ms": 1250.5,
                "model_used": "ibm/granite-20b-code-instruct",
                "created_at": "2024-01-15T10:30:00Z",
                "completed_at": "2024-01-15T10:30:01Z"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    watsonx_connected: bool = Field(..., description="Whether watsonx.ai is accessible")
    mock_mode: bool = Field(..., description="Whether running in mock mode")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "watsonx-ai-integration",
                "version": "1.0.0",
                "watsonx_connected": True,
                "mock_mode": False
            }
        }

# Made with Bob