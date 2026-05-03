"""
Inefficient pattern detector
"""

import ast
from typing import List, Dict
from ..utils.logger import get_logger
from ..utils.ast_helpers import (
    get_loop_nodes,
    count_nested_loops,
    get_recursive_calls,
    has_memoization,
    get_function_calls
)
from ..models.response import InefficientPattern

logger = get_logger(__name__)


class PatternAnalyzer:
    """Detects common inefficient code patterns"""
    
    def __init__(self):
        self.patterns = []
    
    def analyze(self, tree: ast.AST) -> List[InefficientPattern]:
        """
        Detect inefficient patterns in code
        
        Args:
            tree: AST to analyze
            
        Returns:
            List of detected inefficient patterns
        """
        self.patterns = []
        
        # Detect nested loops
        self._detect_nested_loops(tree)
        
        # Detect redundant recursion
        self._detect_redundant_recursion(tree)
        
        # Detect linear search in loops
        self._detect_linear_search_in_loop(tree)
        
        # Detect repeated sorting
        self._detect_repeated_sorting(tree)
        
        # Detect string concatenation in loops
        self._detect_string_concatenation_in_loop(tree)
        
        # Detect list operations in loops
        self._detect_list_operations_in_loop(tree)
        
        return self.patterns
    
    def _detect_nested_loops(self, tree: ast.AST) -> None:
        """Detect nested loops pattern"""
        max_depth = count_nested_loops(tree)
        
        if max_depth >= 2:
            # Find the nested loop locations
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While)):
                    # Check if this loop contains another loop
                    inner_loops = []
                    for child in ast.walk(node):
                        if child != node and isinstance(child, (ast.For, ast.While)):
                            inner_loops.append(child)
                    
                    if inner_loops:
                        line_numbers = [getattr(node, 'lineno', 0)]
                        for inner in inner_loops[:1]:  # Just first inner loop
                            line_numbers.append(getattr(inner, 'lineno', 0))
                        
                        severity = 'high' if max_depth >= 3 else 'medium'
                        
                        self.patterns.append(InefficientPattern(
                            pattern_type='nested_loops',
                            severity=severity,
                            line_numbers=line_numbers,
                            description=f'Nested loops with {max_depth} levels of nesting',
                            impact=f'O(n^{max_depth}) time complexity - performance degrades exponentially'
                        ))
                        break  # Only report once
    
    def _detect_redundant_recursion(self, tree: ast.AST) -> None:
        """Detect recursion without memoization"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                recursive_calls = get_recursive_calls(node)
                
                if len(recursive_calls) >= 2 and not has_memoization(node):
                    line_numbers = [getattr(node, 'lineno', 0)]
                    
                    self.patterns.append(InefficientPattern(
                        pattern_type='redundant_recursion',
                        severity='high',
                        line_numbers=line_numbers,
                        description='Multiple recursive calls without memoization',
                        impact='Exponential time complexity O(2^n) - redundant calculations'
                    ))
    
    def _detect_linear_search_in_loop(self, tree: ast.AST) -> None:
        """Detect linear search operations inside loops"""
        loops = get_loop_nodes(tree)
        
        for loop in loops:
            # Check for 'in' operator with lists
            for node in ast.walk(loop):
                if isinstance(node, ast.Compare):
                    for op in node.ops:
                        if isinstance(op, (ast.In, ast.NotIn)):
                            # Check if comparing against a list/array
                            line_no = getattr(node, 'lineno', 0)
                            
                            self.patterns.append(InefficientPattern(
                                pattern_type='linear_search_in_loop',
                                severity='medium',
                                line_numbers=[line_no],
                                description='Linear search (in operator) inside a loop',
                                impact='O(n²) time complexity - use set or dict for O(1) lookups'
                            ))
                            break
    
    def _detect_repeated_sorting(self, tree: ast.AST) -> None:
        """Detect multiple sorting operations"""
        sort_calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'sort':
                        line_no = getattr(node, 'lineno', 0)
                        sort_calls.append(line_no)
                elif isinstance(node.func, ast.Name):
                    if node.func.id == 'sorted':
                        line_no = getattr(node, 'lineno', 0)
                        sort_calls.append(line_no)
        
        if len(sort_calls) > 1:
            self.patterns.append(InefficientPattern(
                pattern_type='repeated_sorting',
                severity='medium',
                line_numbers=sort_calls,
                description='Multiple sorting operations detected',
                impact='O(n log n) per sort - consider sorting once and maintaining order'
            ))
    
    def _detect_string_concatenation_in_loop(self, tree: ast.AST) -> None:
        """Detect string concatenation inside loops"""
        loops = get_loop_nodes(tree)
        
        for loop in loops:
            for node in ast.walk(loop):
                # Check for += with strings
                if isinstance(node, ast.AugAssign):
                    if isinstance(node.op, ast.Add):
                        line_no = getattr(node, 'lineno', 0)
                        
                        self.patterns.append(InefficientPattern(
                            pattern_type='string_concatenation_in_loop',
                            severity='medium',
                            line_numbers=[line_no],
                            description='String concatenation inside a loop',
                            impact='O(n²) due to string immutability - use list and join() instead'
                        ))
                        break
    
    def _detect_list_operations_in_loop(self, tree: ast.AST) -> None:
        """Detect inefficient list operations in loops"""
        loops = get_loop_nodes(tree)
        
        for loop in loops:
            for node in ast.walk(loop):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute):
                        method = node.func.attr
                        
                        # Check for insert(0, ...) or pop(0)
                        if method in ['insert', 'pop']:
                            if node.args and isinstance(node.args[0], ast.Constant):
                                if node.args[0].value == 0:
                                    line_no = getattr(node, 'lineno', 0)
                                    
                                    self.patterns.append(InefficientPattern(
                                        pattern_type='inefficient_list_operation',
                                        severity='medium',
                                        line_numbers=[line_no],
                                        description=f'List.{method}(0) inside a loop',
                                        impact='O(n) per operation - use deque for O(1) operations at both ends'
                                    ))

# Made with Bob
