"""
Time complexity analyzer
"""

import ast
from typing import Dict, List, Tuple
from ..utils.logger import get_logger
from ..utils.ast_helpers import (
    get_loop_nodes,
    get_recursive_calls,
    count_nested_loops,
    get_function_calls,
    has_memoization
)

logger = get_logger(__name__)


class TimeComplexityAnalyzer:
    """Analyzes time complexity of code"""
    
    # Built-in function complexities
    BUILTIN_COMPLEXITIES = {
        'len': 'O(1)',
        'append': 'O(1)',
        'pop': 'O(1)',
        'insert': 'O(n)',
        'remove': 'O(n)',
        'index': 'O(n)',
        'count': 'O(n)',
        'sort': 'O(n log n)',
        'sorted': 'O(n log n)',
        'min': 'O(n)',
        'max': 'O(n)',
        'sum': 'O(n)',
        'reversed': 'O(n)',
        'enumerate': 'O(1)',
        'zip': 'O(1)',
        'map': 'O(1)',
        'filter': 'O(1)',
        'any': 'O(n)',
        'all': 'O(n)',
        'in': 'O(n)',  # for lists
    }
    
    def __init__(self):
        self.complexity_factors = []
    
    def analyze(self, tree: ast.AST) -> Tuple[str, List[str]]:
        """
        Analyze time complexity of code
        
        Args:
            tree: AST to analyze
            
        Returns:
            Tuple of (complexity_notation, factors_list)
        """
        self.complexity_factors = []
        
        # Analyze functions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._analyze_function(node)
        
        # If no functions, analyze top-level code
        if not self.complexity_factors:
            self._analyze_node(tree)
        
        # Calculate overall complexity
        complexity = self._calculate_overall_complexity()
        
        return complexity, self.complexity_factors
    
    def _analyze_function(self, func_node: ast.FunctionDef) -> None:
        """Analyze a single function"""
        # Check for recursion
        recursive_calls = get_recursive_calls(func_node)
        if recursive_calls:
            self._analyze_recursion(func_node, recursive_calls)
        
        # Analyze loops
        self._analyze_loops(func_node)
        
        # Analyze function calls
        self._analyze_function_calls(func_node)
    
    def _analyze_node(self, node: ast.AST) -> None:
        """Analyze a general AST node"""
        # Analyze loops
        self._analyze_loops(node)
        
        # Analyze function calls
        self._analyze_function_calls(node)
    
    def _analyze_loops(self, node: ast.AST) -> None:
        """Analyze loop complexity"""
        loops = get_loop_nodes(node)
        
        if not loops:
            return
        
        # Count nesting depth
        max_depth = count_nested_loops(node)
        
        if max_depth == 1:
            self.complexity_factors.append("Single loop: O(n)")
        elif max_depth == 2:
            self.complexity_factors.append("Nested loops (2 levels): O(n²)")
        elif max_depth == 3:
            self.complexity_factors.append("Nested loops (3 levels): O(n³)")
        elif max_depth > 3:
            self.complexity_factors.append(f"Nested loops ({max_depth} levels): O(n^{max_depth})")
        
        # Analyze individual loops
        for loop in loops:
            self._analyze_single_loop(loop)
    
    def _analyze_single_loop(self, loop_node: ast.AST) -> None:
        """Analyze a single loop"""
        if isinstance(loop_node, ast.For):
            # Check if it's a range loop
            if isinstance(loop_node.iter, ast.Call):
                if isinstance(loop_node.iter.func, ast.Name):
                    func_name = loop_node.iter.func.id
                    if func_name == 'range':
                        # Analyze range arguments
                        args = loop_node.iter.args
                        if len(args) == 1:
                            self.complexity_factors.append("Loop iterates n times")
                        elif len(args) >= 2:
                            # Could be range(0, n) or range(start, end)
                            self.complexity_factors.append("Loop with range iteration")
    
    def _analyze_recursion(self, func_node: ast.FunctionDef, recursive_calls: List[ast.Call]) -> None:
        """Analyze recursive function complexity"""
        # Check for memoization
        if has_memoization(func_node):
            self.complexity_factors.append("Recursive with memoization: O(n)")
            return
        
        # Count recursive calls per invocation
        num_calls = len(recursive_calls)
        
        if num_calls == 1:
            # Linear recursion (e.g., factorial)
            self.complexity_factors.append("Linear recursion: O(n)")
        elif num_calls == 2:
            # Binary recursion (e.g., fibonacci)
            self.complexity_factors.append("Binary recursion without memoization: O(2^n)")
        else:
            # Multiple recursive calls
            self.complexity_factors.append(f"Multiple recursive calls ({num_calls}): O({num_calls}^n)")
    
    def _analyze_function_calls(self, node: ast.AST) -> None:
        """Analyze complexity of function calls"""
        calls = get_function_calls(node)
        
        for func_name, _ in calls:
            if func_name in self.BUILTIN_COMPLEXITIES:
                complexity = self.BUILTIN_COMPLEXITIES[func_name]
                if complexity != 'O(1)':
                    self.complexity_factors.append(f"{func_name}() call: {complexity}")
    
    def _calculate_overall_complexity(self) -> str:
        """Calculate overall time complexity from factors"""
        if not self.complexity_factors:
            return "O(1)"
        
        # Look for dominant complexity
        complexity_order = {
            'O(1)': 0,
            'O(log n)': 1,
            'O(n)': 2,
            'O(n log n)': 3,
            'O(n²)': 4,
            'O(n³)': 5,
            'O(2^n)': 6,
        }
        
        max_complexity = 'O(1)'
        max_order = 0
        
        for factor in self.complexity_factors:
            # Extract complexity notation from factor
            if 'O(n³)' in factor or '3 levels' in factor:
                if complexity_order.get('O(n³)', 5) > max_order:
                    max_complexity = 'O(n³)'
                    max_order = 5
            elif 'O(n²)' in factor or '2 levels' in factor or 'Nested loops' in factor:
                if complexity_order.get('O(n²)', 4) > max_order:
                    max_complexity = 'O(n²)'
                    max_order = 4
            elif 'O(2^n)' in factor or 'Binary recursion without memoization' in factor:
                if complexity_order.get('O(2^n)', 6) > max_order:
                    max_complexity = 'O(2^n)'
                    max_order = 6
            elif 'O(n log n)' in factor:
                if complexity_order.get('O(n log n)', 3) > max_order:
                    max_complexity = 'O(n log n)'
                    max_order = 3
            elif 'O(n)' in factor:
                if complexity_order.get('O(n)', 2) > max_order:
                    max_complexity = 'O(n)'
                    max_order = 2
            elif 'O(log n)' in factor:
                if complexity_order.get('O(log n)', 1) > max_order:
                    max_complexity = 'O(log n)'
                    max_order = 1
        
        return max_complexity
    
    def get_target_complexity(self, current_complexity: str) -> str:
        """
        Determine achievable target complexity
        
        Args:
            current_complexity: Current complexity notation
            
        Returns:
            Target complexity notation
        """
        # Mapping of current to target complexities
        targets = {
            'O(2^n)': 'O(n)',  # With memoization
            'O(n³)': 'O(n²)',  # Reduce nesting
            'O(n²)': 'O(n)',   # Use hash maps or better algorithms
            'O(n log n)': 'O(n)',  # If sorting can be avoided
            'O(n)': 'O(log n)',  # With binary search on sorted data
            'O(log n)': 'O(1)',  # With hash maps
            'O(1)': 'O(1)'  # Already optimal
        }
        
        return targets.get(current_complexity, current_complexity)

# Made with Bob
