"""
Data models for Efficiency Analyzer service
"""

from .request import CodeAnalysisRequest
from .response import (
    EfficiencyReport,
    InefficientPattern,
    OptimizationStrategy,
    ComplexityInfo
)

__all__ = [
    "CodeAnalysisRequest",
    "EfficiencyReport",
    "InefficientPattern",
    "OptimizationStrategy",
    "ComplexityInfo"
]

# Made with Bob
