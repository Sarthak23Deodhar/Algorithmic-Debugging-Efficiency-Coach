"""
Pattern detector service
"""

from typing import List
from ..models.response import InefficientPattern
from ..analyzers.patterns import PatternAnalyzer
from ..utils.logger import get_logger
from ..utils.ast_helpers import parse_python_code

logger = get_logger(__name__)


class PatternDetector:
    """Detects inefficient code patterns"""
    
    def __init__(self):
        self.pattern_analyzer = PatternAnalyzer()
    
    def detect_patterns(self, code: str, language: str) -> List[InefficientPattern]:
        """
        Detect inefficient patterns in code
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            List of detected inefficient patterns
        """
        if language != "python":
            logger.warning(f"Language {language} not fully supported for pattern detection")
            return []
        
        # Parse code
        tree = parse_python_code(code)
        if tree is None:
            logger.error("Failed to parse code for pattern detection")
            return []
        
        # Detect patterns
        patterns = self.pattern_analyzer.analyze(tree)
        
        logger.info(f"Detected {len(patterns)} inefficient patterns")
        
        return patterns

# Made with Bob
