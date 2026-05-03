"""
Space complexity analyzer
"""

import ast
from typing import Dict, List, Tuple
from ..utils.logger import get_logger
from ..utils.ast_helpers import (
    analyze_data_structures,
    get_recursive_calls,
    get_comprehensions
)

logger = get_logger(__name__)


class SpaceComplexityAnalyzer:
    """Analyzes space complexity of code"""
    
    def __init__(self):
        self.complexity_factors = []
    
    def analyze(self, tree: ast.AST) -> Tuple[str, List[str]]:
        """
        Analyze space complexity of code
        
        Args:
            tree: AST to analyze
            
        Returns:
            Tuple of (complexity_notation, factors_list)
        """
        self.complexity_factors = []
        
        # Analyze data structures
        data_structures = analyze_data_structures(tree)
        self._analyze_data_structures(data_structures)
        
        # Analyze recursion (call stack)
        self._analyze_recursion(tree)
        
        # Analyze comprehensions
        self._analyze_comprehensions(tree)
        
        # Calculate overall complexity
        complexity = self._calculate_overall_complexity()
        
        return complexity, self.complexity_factors
    
    def _analyze_data_structures(self, data_structures: Dict[str, List[str]]) -> None:
        """Analyze space used by data structures"""
        total_structures = sum(len(vars) for vars in data_structures.values())
        
        if total_structures == 0:
            self.complexity_factors.append("No auxiliary data structures: O(1)")
            return
        
        # Lists, dicts, sets typically use O(n) space
        for ds_type, vars in data_structures.items():
            if vars:
                if ds_type in ['list', 'dict', 'set']:
                    self.complexity_factors.append(
                        f"{ds_type.capitalize()} data structure(s): O(n) space"
                    )
    
    def _analyze_recursion(self, tree: ast.AST) -> None:
        """Analyze space used by recursion (call stack)"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                recursive_calls = get_recursive_calls(node)
                if recursive_calls:
                    # Recursive functions use call stack space
                    self.complexity_factors.append(
                        "Recursive call stack: O(n) space"
                    )
                    break
    
    def _analyze_comprehensions(self, tree: ast.AST) -> None:
        """Analyze space used by comprehensions"""
        comprehensions = get_comprehensions(tree)
        
        for comp in comprehensions:
            if isinstance(comp, ast.ListComp):
                self.complexity_factors.append(
                    "List comprehension creates new list: O(n) space"
                )
            elif isinstance(comp, ast.DictComp):
                self.complexity_factors.append(
                    "Dict comprehension creates new dict: O(n) space"
                )
            elif isinstance(comp, ast.SetComp):
                self.complexity_factors.append(
                    "Set comprehension creates new set: O(n) space"
                )
            elif isinstance(comp, ast.GeneratorExp):
                # Generators are space-efficient
                self.complexity_factors.append(
                    "Generator expression: O(1) space (lazy evaluation)"
                )
    
    def _calculate_overall_complexity(self) -> str:
        """Calculate overall space complexity from factors"""
        if not self.complexity_factors:
            return "O(1)"
        
        # Check if any factor indicates O(n) space
        for factor in self.complexity_factors:
            if 'O(n)' in factor:
                return "O(n)"
        
        # Otherwise, it's constant space
        return "O(1)"
    
    def get_target_complexity(self, current_complexity: str) -> str:
        """
        Determine achievable target space complexity
        
        Args:
            current_complexity: Current complexity notation
            
        Returns:
            Target complexity notation
        """
        # Space complexity is harder to optimize than time
        # Usually O(n) space is acceptable
        if current_complexity == "O(n)":
            return "O(1)"  # If we can use in-place operations
        return current_complexity

# Made with Bob
