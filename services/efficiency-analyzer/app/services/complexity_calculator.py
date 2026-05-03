"""
Complexity calculator service
"""

from typing import Tuple, List
from ..models.response import ComplexityInfo
from ..analyzers.time_complexity import TimeComplexityAnalyzer
from ..analyzers.space_complexity import SpaceComplexityAnalyzer
from ..utils.logger import get_logger
from ..utils.ast_helpers import parse_python_code
import ast

logger = get_logger(__name__)


class ComplexityCalculator:
    """Calculates time and space complexity of code"""
    
    def __init__(self):
        self.time_analyzer = TimeComplexityAnalyzer()
        self.space_analyzer = SpaceComplexityAnalyzer()
    
    def calculate_complexity(
        self,
        code: str,
        language: str
    ) -> Tuple[ComplexityInfo, ComplexityInfo, str, str]:
        """
        Calculate time and space complexity
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Tuple of (time_complexity_info, space_complexity_info, 
                     target_time_complexity, target_space_complexity)
        """
        if language != "python":
            # For now, only Python is fully supported
            logger.warning(f"Language {language} not fully supported, using basic analysis")
            return self._basic_complexity_analysis()
        
        # Parse code
        tree = parse_python_code(code)
        if tree is None:
            logger.error("Failed to parse code")
            return self._basic_complexity_analysis()
        
        # Analyze time complexity
        time_notation, time_factors = self.time_analyzer.analyze(tree)
        time_complexity = ComplexityInfo(
            notation=time_notation,
            explanation=self._generate_time_explanation(time_notation, time_factors),
            factors=time_factors
        )
        
        # Analyze space complexity
        space_notation, space_factors = self.space_analyzer.analyze(tree)
        space_complexity = ComplexityInfo(
            notation=space_notation,
            explanation=self._generate_space_explanation(space_notation, space_factors),
            factors=space_factors
        )
        
        # Determine target complexities
        target_time = self.time_analyzer.get_target_complexity(time_notation)
        target_space = self.space_analyzer.get_target_complexity(space_notation)
        
        return time_complexity, space_complexity, target_time, target_space
    
    def _generate_time_explanation(self, notation: str, factors: List[str]) -> str:
        """Generate human-readable explanation of time complexity"""
        explanations = {
            'O(1)': 'Constant time - executes in fixed time regardless of input size',
            'O(log n)': 'Logarithmic time - typically from binary search or divide-and-conquer',
            'O(n)': 'Linear time - processes each element once',
            'O(n log n)': 'Linearithmic time - typical of efficient sorting algorithms',
            'O(n²)': 'Quadratic time - nested iterations over the data',
            'O(n³)': 'Cubic time - triple nested iterations',
            'O(2^n)': 'Exponential time - typically from unoptimized recursion'
        }
        
        base_explanation = explanations.get(notation, f'Time complexity is {notation}')
        
        if factors:
            return f"{base_explanation}. Contributing factors: {', '.join(factors[:3])}"
        
        return base_explanation
    
    def _generate_space_explanation(self, notation: str, factors: List[str]) -> str:
        """Generate human-readable explanation of space complexity"""
        explanations = {
            'O(1)': 'Constant space - uses fixed amount of memory',
            'O(n)': 'Linear space - memory usage grows with input size'
        }
        
        base_explanation = explanations.get(notation, f'Space complexity is {notation}')
        
        if factors:
            return f"{base_explanation}. Contributing factors: {', '.join(factors[:3])}"
        
        return base_explanation
    
    def _basic_complexity_analysis(self) -> Tuple[ComplexityInfo, ComplexityInfo, str, str]:
        """Return basic complexity analysis when parsing fails"""
        time_complexity = ComplexityInfo(
            notation='O(n)',
            explanation='Unable to perform detailed analysis',
            factors=['Analysis limited due to parsing error']
        )
        
        space_complexity = ComplexityInfo(
            notation='O(1)',
            explanation='Unable to perform detailed analysis',
            factors=['Analysis limited due to parsing error']
        )
        
        return time_complexity, space_complexity, 'O(n)', 'O(1)'

# Made with Bob
