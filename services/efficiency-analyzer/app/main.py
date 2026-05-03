"""
FastAPI application for Efficiency Analyzer service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import traceback

from .models.request import CodeAnalysisRequest
from .models.response import EfficiencyReport
from .services.complexity_calculator import ComplexityCalculator
from .services.pattern_detector import PatternDetector
from .services.optimizer import Optimizer
from .utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Efficiency Analyzer Service",
    description="Analyzes code complexity and recommends optimizations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
complexity_calculator = ComplexityCalculator()
pattern_detector = PatternDetector()
optimizer = Optimizer()


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    
    Returns:
        Status information
    """
    return {
        "status": "healthy",
        "service": "efficiency-analyzer",
        "version": "1.0.0"
    }


@app.post("/api/v1/analyze", response_model=EfficiencyReport)
async def analyze_code(request: CodeAnalysisRequest) -> EfficiencyReport:
    """
    Analyze code for efficiency and provide optimization recommendations
    
    Args:
        request: Code analysis request containing code and language
        
    Returns:
        Efficiency analysis report with complexity and optimization strategies
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        logger.info(f"Analyzing {request.language} code ({len(request.code)} characters)")
        
        # Calculate complexity
        (
            time_complexity,
            space_complexity,
            target_time,
            target_space
        ) = complexity_calculator.calculate_complexity(
            request.code,
            request.language.value
        )
        
        # Detect inefficient patterns
        patterns = pattern_detector.detect_patterns(
            request.code,
            request.language.value
        )
        
        # Get optimization strategies
        strategies = optimizer.recommend_strategies(
            time_complexity.notation,
            patterns
        )
        
        # Estimate improvement
        estimated_improvement = optimizer.estimate_improvement(
            time_complexity.notation,
            target_time
        )
        
        # Calculate overall efficiency score (0-100)
        overall_score = _calculate_efficiency_score(
            time_complexity.notation,
            len(patterns)
        )
        
        # Build report
        report = EfficiencyReport(
            current_time_complexity=time_complexity,
            current_space_complexity=space_complexity,
            target_time_complexity=target_time,
            target_space_complexity=target_space,
            inefficient_patterns=patterns,
            optimization_strategies=strategies,
            estimated_improvement=estimated_improvement,
            overall_score=overall_score
        )
        
        logger.info(
            f"Analysis complete: {time_complexity.notation} time, "
            f"{space_complexity.notation} space, "
            f"{len(patterns)} patterns, "
            f"score: {overall_score}"
        )
        
        return report
        
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze code: {str(e)}"
        )


def _calculate_efficiency_score(complexity: str, pattern_count: int) -> int:
    """
    Calculate overall efficiency score (0-100)
    
    Args:
        complexity: Time complexity notation
        pattern_count: Number of inefficient patterns detected
        
    Returns:
        Efficiency score (higher is better)
    """
    # Base score from complexity
    complexity_scores = {
        'O(1)': 100,
        'O(log n)': 90,
        'O(n)': 75,
        'O(n log n)': 60,
        'O(n²)': 35,
        'O(n³)': 15,
        'O(2^n)': 5
    }
    
    base_score = complexity_scores.get(complexity, 50)
    
    # Deduct points for patterns (max 5 points per pattern)
    pattern_penalty = min(pattern_count * 5, 30)
    
    final_score = max(0, base_score - pattern_penalty)
    
    return final_score


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint with service information
    
    Returns:
        Service information
    """
    return {
        "service": "Efficiency Analyzer",
        "version": "1.0.0",
        "description": "Analyzes code complexity and recommends optimizations",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/v1/analyze"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

# Made with Bob
