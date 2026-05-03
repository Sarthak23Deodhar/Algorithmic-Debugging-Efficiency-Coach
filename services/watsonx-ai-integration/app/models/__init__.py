"""
Models package for watsonx.ai Integration service
"""

from .request import (
    ProgrammingLanguage,
    CodeGenerationRequest,
    RefactoringRequest,
    ExplanationRequest,
    OperationType,
    OptimizationTarget
)
from .response import (
    AIResponse,
    JobStatus,
    GeneratedCode,
    RefactoredCode,
    CodeExplanation,
    HealthResponse
)

__all__ = [
    "ProgrammingLanguage",
    "CodeGenerationRequest",
    "RefactoringRequest",
    "ExplanationRequest",
    "OperationType",
    "OptimizationTarget",
    "AIResponse",
    "JobStatus",
    "GeneratedCode",
    "RefactoredCode",
    "CodeExplanation",
    "HealthResponse"
]

# Made with Bob