"""
Response models for Efficiency Analyzer service
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ComplexityInfo(BaseModel):
    """Information about complexity analysis"""
    
    notation: str = Field(
        ...,
        description="Big O notation (e.g., O(n), O(n²), O(log n))"
    )
    
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the complexity"
    )
    
    factors: List[str] = Field(
        default_factory=list,
        description="Contributing factors to this complexity"
    )


class InefficientPattern(BaseModel):
    """Detected inefficient code pattern"""
    
    pattern_type: str = Field(
        ...,
        description="Type of inefficient pattern (e.g., 'nested_loops', 'redundant_recursion')"
    )
    
    severity: str = Field(
        ...,
        description="Severity level: 'high', 'medium', or 'low'"
    )
    
    line_numbers: List[int] = Field(
        ...,
        description="Line numbers where the pattern occurs"
    )
    
    description: str = Field(
        ...,
        description="Description of the inefficiency"
    )
    
    impact: str = Field(
        ...,
        description="Performance impact of this pattern"
    )


class OptimizationStrategy(BaseModel):
    """Recommended optimization strategy"""
    
    technique: str = Field(
        ...,
        description="Optimization technique (e.g., 'Dynamic Programming', 'Hash Map')"
    )
    
    description: str = Field(
        ...,
        description="Detailed description of the optimization"
    )
    
    steps: List[str] = Field(
        ...,
        description="Step-by-step implementation guide"
    )
    
    complexity_improvement: str = Field(
        ...,
        description="Expected complexity improvement (e.g., 'O(n²) → O(n)')"
    )
    
    code_example: Optional[str] = Field(
        None,
        description="Example code snippet showing the optimization"
    )


class EfficiencyReport(BaseModel):
    """Complete efficiency analysis report"""
    
    current_time_complexity: ComplexityInfo = Field(
        ...,
        description="Current time complexity analysis"
    )
    
    current_space_complexity: ComplexityInfo = Field(
        ...,
        description="Current space complexity analysis"
    )
    
    target_time_complexity: str = Field(
        ...,
        description="Achievable target time complexity"
    )
    
    target_space_complexity: str = Field(
        ...,
        description="Achievable target space complexity"
    )
    
    inefficient_patterns: List[InefficientPattern] = Field(
        default_factory=list,
        description="List of detected inefficient patterns"
    )
    
    optimization_strategies: List[OptimizationStrategy] = Field(
        default_factory=list,
        description="Recommended optimization strategies"
    )
    
    estimated_improvement: Dict[str, str] = Field(
        default_factory=dict,
        description="Estimated performance improvements for different input sizes"
    )
    
    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall efficiency score (0-100)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_time_complexity": {
                    "notation": "O(n²)",
                    "explanation": "Nested loops iterate over the array",
                    "factors": ["Outer loop: O(n)", "Inner loop: O(n)", "Combined: O(n²)"]
                },
                "current_space_complexity": {
                    "notation": "O(n)",
                    "explanation": "Additional list to store duplicates",
                    "factors": ["Duplicates list: O(n)"]
                },
                "target_time_complexity": "O(n)",
                "target_space_complexity": "O(n)",
                "inefficient_patterns": [
                    {
                        "pattern_type": "nested_loops",
                        "severity": "high",
                        "line_numbers": [3, 4],
                        "description": "Nested loops with O(n²) complexity",
                        "impact": "Performance degrades quadratically with input size"
                    }
                ],
                "optimization_strategies": [
                    {
                        "technique": "Hash Set",
                        "description": "Use a set to track seen elements in O(1) time",
                        "steps": [
                            "Create an empty set to track seen elements",
                            "Iterate through array once",
                            "Check if element exists in set (O(1))",
                            "Add to result if duplicate found"
                        ],
                        "complexity_improvement": "O(n²) → O(n)",
                        "code_example": "def find_duplicates(arr):\n    seen = set()\n    duplicates = set()\n    for num in arr:\n        if num in seen:\n            duplicates.add(num)\n        seen.add(num)\n    return list(duplicates)"
                    }
                ],
                "estimated_improvement": {
                    "n=100": "10x faster",
                    "n=1000": "100x faster",
                    "n=10000": "1000x faster"
                },
                "overall_score": 35
            }
        }

# Made with Bob
