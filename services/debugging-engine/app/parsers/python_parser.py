"""
Python code parser using built-in ast module
"""

import ast
from typing import Dict, List, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class PythonParser:
    """
    Parser for Python code using the built-in ast module
    """
    
    def __init__(self):
        """Initialize the Python parser"""
        self.tree: Optional[ast.AST] = None
        self.source_lines: List[str] = []
    
    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code and extract structural information
        
        Args:
            code: Python source code as string
            
        Returns:
            Dictionary containing parsed information
            
        Raises:
            SyntaxError: If the code has syntax errors
        """
        self.source_lines = code.split('\n')
        
        try:
            self.tree = ast.parse(code)
            
            return {
                'success': True,
                'functions': self._extract_functions(),
                'classes': self._extract_classes(),
                'imports': self._extract_imports(),
                'variables': self._extract_variables(),
                'control_structures': self._extract_control_structures(),
                'syntax_errors': []
            }
        except SyntaxError as e:
            logger.error(f"Syntax error in Python code: {e}")
            return {
                'success': False,
                'functions': [],
                'classes': [],
                'imports': [],
                'variables': [],
                'control_structures': [],
                'syntax_errors': [{
                    'line': e.lineno or 0,
                    'column': e.offset or 0,
                    'message': str(e.msg),
                    'text': e.text or ''
                }]
            }
    
    def _extract_functions(self) -> List[Dict[str, Any]]:
        """Extract function definitions from the AST"""
        functions = []
        
        if not self.tree:
            return functions
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'params': [arg.arg for arg in node.args.args],
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
                    'is_async': False
                })
            elif isinstance(node, ast.AsyncFunctionDef):
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'params': [arg.arg for arg in node.args.args],
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
                    'is_async': True
                })
        
        return functions
    
    def _extract_classes(self) -> List[Dict[str, Any]]:
        """Extract class definitions from the AST"""
        classes = []
        
        if not self.tree:
            return classes
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)
                
                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'bases': [self._get_name(base) for base in node.bases],
                    'methods': methods,
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
                })
        
        return classes
    
    def _extract_imports(self) -> List[Dict[str, Any]]:
        """Extract import statements from the AST"""
        imports = []
        
        if not self.tree:
            return imports
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        'type': 'from_import',
                        'module': node.module or '',
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
        
        return imports
    
    def _extract_variables(self) -> List[Dict[str, Any]]:
        """Extract variable assignments from the AST"""
        variables = []
        
        if not self.tree:
            return variables
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append({
                            'name': target.id,
                            'line': node.lineno,
                            'scope': 'global'  # Simplified; would need scope analysis
                        })
        
        return variables
    
    def _extract_control_structures(self) -> List[Dict[str, Any]]:
        """Extract control flow structures (if, for, while, etc.)"""
        structures = []
        
        if not self.tree:
            return structures
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                structures.append({
                    'type': 'if',
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'has_else': len(node.orelse) > 0
                })
            elif isinstance(node, ast.For):
                structures.append({
                    'type': 'for',
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'target': self._get_name(node.target),
                    'has_else': len(node.orelse) > 0
                })
            elif isinstance(node, ast.While):
                structures.append({
                    'type': 'while',
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'has_else': len(node.orelse) > 0
                })
            elif isinstance(node, ast.Try):
                structures.append({
                    'type': 'try',
                    'line': node.lineno,
                    'end_line': node.end_lineno,
                    'handlers': len(node.handlers),
                    'has_finally': len(node.finalbody) > 0
                })
        
        return structures
    
    def _get_name(self, node: ast.AST) -> str:
        """Get the name from an AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
    
    def _get_decorator_name(self, node: ast.AST) -> str:
        """Get decorator name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)

# Made with Bob
