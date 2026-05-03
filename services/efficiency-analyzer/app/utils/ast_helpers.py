"""
AST utility functions for code analysis
"""

import ast
from typing import List, Dict, Optional, Set, Tuple
from .logger import get_logger

logger = get_logger(__name__)


def parse_python_code(code: str) -> Optional[ast.AST]:
    """
    Parse Python code into an AST
    
    Args:
        code: Python source code
        
    Returns:
        AST node or None if parsing fails
    """
    try:
        return ast.parse(code)
    except SyntaxError as e:
        logger.error(f"Syntax error parsing code: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing code: {e}")
        return None


def get_function_nodes(tree: ast.AST) -> List[ast.FunctionDef]:
    """
    Extract all function definition nodes from AST
    
    Args:
        tree: AST to analyze
        
    Returns:
        List of function definition nodes
    """
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node)
    return functions


def get_loop_nodes(node: ast.AST) -> List[ast.AST]:
    """
    Extract all loop nodes (For, While) from AST
    
    Args:
        node: AST node to analyze
        
    Returns:
        List of loop nodes
    """
    loops = []
    for child in ast.walk(node):
        if isinstance(child, (ast.For, ast.While)):
            loops.append(child)
    return loops


def get_recursive_calls(func_node: ast.FunctionDef) -> List[ast.Call]:
    """
    Find recursive calls within a function
    
    Args:
        func_node: Function definition node
        
    Returns:
        List of recursive call nodes
    """
    func_name = func_node.name
    recursive_calls = []
    
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == func_name:
                recursive_calls.append(node)
    
    return recursive_calls


def count_nested_loops(node: ast.AST) -> int:
    """
    Count maximum nesting level of loops
    
    Args:
        node: AST node to analyze
        
    Returns:
        Maximum nesting depth
    """
    def _count_depth(n: ast.AST, current_depth: int = 0) -> int:
        max_depth = current_depth
        
        for child in ast.iter_child_nodes(n):
            if isinstance(child, (ast.For, ast.While)):
                depth = _count_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = _count_depth(child, current_depth)
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    return _count_depth(node)


def get_loop_variable(loop_node: ast.For) -> Optional[str]:
    """
    Get the loop variable name from a For loop
    
    Args:
        loop_node: For loop node
        
    Returns:
        Variable name or None
    """
    if isinstance(loop_node.target, ast.Name):
        return loop_node.target.id
    return None


def get_loop_iterable(loop_node: ast.For) -> Optional[str]:
    """
    Get the iterable expression from a For loop
    
    Args:
        loop_node: For loop node
        
    Returns:
        Iterable name or None
    """
    if isinstance(loop_node.iter, ast.Name):
        return loop_node.iter.id
    elif isinstance(loop_node.iter, ast.Call):
        if isinstance(loop_node.iter.func, ast.Name):
            return loop_node.iter.func.id
    return None


def analyze_data_structures(tree: ast.AST) -> Dict[str, List[str]]:
    """
    Analyze data structure usage in code
    
    Args:
        tree: AST to analyze
        
    Returns:
        Dictionary mapping data structure types to variable names
    """
    data_structures = {
        'list': [],
        'dict': [],
        'set': [],
        'tuple': []
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    
                    # Check value type
                    if isinstance(node.value, ast.List):
                        data_structures['list'].append(var_name)
                    elif isinstance(node.value, ast.Dict):
                        data_structures['dict'].append(var_name)
                    elif isinstance(node.value, ast.Set):
                        data_structures['set'].append(var_name)
                    elif isinstance(node.value, ast.Tuple):
                        data_structures['tuple'].append(var_name)
                    elif isinstance(node.value, ast.Call):
                        if isinstance(node.value.func, ast.Name):
                            func_name = node.value.func.id
                            if func_name in ['list', 'dict', 'set', 'tuple']:
                                data_structures[func_name].append(var_name)
    
    return data_structures


def get_function_calls(node: ast.AST) -> List[Tuple[str, int]]:
    """
    Get all function calls with their line numbers
    
    Args:
        node: AST node to analyze
        
    Returns:
        List of (function_name, line_number) tuples
    """
    calls = []
    
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                func_name = child.func.id
                line_no = getattr(child, 'lineno', 0)
                calls.append((func_name, line_no))
            elif isinstance(child.func, ast.Attribute):
                method_name = child.func.attr
                line_no = getattr(child, 'lineno', 0)
                calls.append((method_name, line_no))
    
    return calls


def has_memoization(func_node: ast.FunctionDef) -> bool:
    """
    Check if a function uses memoization
    
    Args:
        func_node: Function definition node
        
    Returns:
        True if memoization is detected
    """
    # Check for @lru_cache decorator
    for decorator in func_node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == 'lru_cache':
            return True
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'lru_cache':
                return True
    
    # Check for manual memoization (cache/memo dict)
    for node in ast.walk(func_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if 'cache' in target.id.lower() or 'memo' in target.id.lower():
                        return True
    
    return False


def get_comprehensions(tree: ast.AST) -> List[ast.AST]:
    """
    Get all list/dict/set comprehensions
    
    Args:
        tree: AST to analyze
        
    Returns:
        List of comprehension nodes
    """
    comprehensions = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            comprehensions.append(node)
    
    return comprehensions

# Made with Bob
