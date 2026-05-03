"""
C++ code parser using tree-sitter
"""

from typing import Dict, List, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)

try:
    from tree_sitter import Language, Parser
    import tree_sitter_cpp as tscpp
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    logger.warning("tree-sitter not available, C++ parsing will be limited")


class CppParser:
    """
    Parser for C++ code using tree-sitter
    """
    
    def __init__(self):
        """Initialize the C++ parser"""
        self.parser: Optional[Any] = None
        self.tree: Optional[Any] = None
        self.source_code: str = ""
        
        if TREE_SITTER_AVAILABLE:
            try:
                CPP_LANGUAGE = Language(tscpp.language())
                self.parser = Parser(CPP_LANGUAGE)
            except Exception as e:
                logger.error(f"Failed to initialize C++ parser: {e}")
                self.parser = None
    
    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse C++ code and extract structural information
        
        Args:
            code: C++ source code as string
            
        Returns:
            Dictionary containing parsed information
        """
        self.source_code = code
        
        if not TREE_SITTER_AVAILABLE or not self.parser:
            return self._fallback_parse(code)
        
        try:
            self.tree = self.parser.parse(bytes(code, "utf8"))
            
            return {
                'success': True,
                'functions': self._extract_functions(),
                'classes': self._extract_classes(),
                'includes': self._extract_includes(),
                'variables': self._extract_variables(),
                'control_structures': self._extract_control_structures(),
                'syntax_errors': self._check_syntax_errors()
            }
        except Exception as e:
            logger.error(f"Error parsing C++ code: {e}")
            return {
                'success': False,
                'functions': [],
                'classes': [],
                'includes': [],
                'variables': [],
                'control_structures': [],
                'syntax_errors': [{'message': str(e), 'line': 0}]
            }
    
    def _fallback_parse(self, code: str) -> Dict[str, Any]:
        """Fallback parsing using simple regex patterns"""
        import re
        
        functions = []
        classes = []
        includes = []
        
        # Extract includes
        for match in re.finditer(r'#include\s*[<"]([^>"]+)[>"]', code):
            includes.append({
                'file': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Extract function declarations (simplified)
        for match in re.finditer(r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{', code):
            functions.append({
                'return_type': match.group(1),
                'name': match.group(2),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Extract class declarations
        for match in re.finditer(r'class\s+(\w+)', code):
            classes.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        return {
            'success': True,
            'functions': functions,
            'classes': classes,
            'includes': includes,
            'variables': [],
            'control_structures': [],
            'syntax_errors': []
        }
    
    def _extract_functions(self) -> List[Dict[str, Any]]:
        """Extract function definitions from the parse tree"""
        if not self.tree:
            return []
        
        functions = []
        
        def traverse(node):
            if node.type == 'function_definition':
                func_info = self._parse_function_node(node)
                if func_info:
                    functions.append(func_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return functions
    
    def _extract_classes(self) -> List[Dict[str, Any]]:
        """Extract class definitions from the parse tree"""
        if not self.tree:
            return []
        
        classes = []
        
        def traverse(node):
            if node.type in ('class_specifier', 'struct_specifier'):
                class_info = self._parse_class_node(node)
                if class_info:
                    classes.append(class_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return classes
    
    def _extract_includes(self) -> List[Dict[str, Any]]:
        """Extract include directives"""
        if not self.tree:
            return []
        
        includes = []
        
        def traverse(node):
            if node.type == 'preproc_include':
                include_info = self._parse_include_node(node)
                if include_info:
                    includes.append(include_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return includes
    
    def _extract_variables(self) -> List[Dict[str, Any]]:
        """Extract variable declarations"""
        if not self.tree:
            return []
        
        variables = []
        
        def traverse(node):
            if node.type == 'declaration':
                var_info = self._parse_variable_node(node)
                if var_info:
                    variables.extend(var_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return variables
    
    def _extract_control_structures(self) -> List[Dict[str, Any]]:
        """Extract control flow structures"""
        if not self.tree:
            return []
        
        structures = []
        
        def traverse(node):
            if node.type in ('if_statement', 'for_statement', 'while_statement', 
                           'do_statement', 'switch_statement'):
                structures.append({
                    'type': node.type.replace('_statement', ''),
                    'line': node.start_point[0] + 1,
                    'end_line': node.end_point[0] + 1
                })
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return structures
    
    def _check_syntax_errors(self) -> List[Dict[str, Any]]:
        """Check for syntax errors in the parse tree"""
        if not self.tree:
            return []
        
        errors = []
        
        def traverse(node):
            if node.type == 'ERROR' or node.is_missing:
                errors.append({
                    'line': node.start_point[0] + 1,
                    'column': node.start_point[1] + 1,
                    'message': f"Syntax error at {node.type}",
                    'text': self._get_node_text(node)
                })
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return errors
    
    def _parse_function_node(self, node) -> Optional[Dict[str, Any]]:
        """Parse a function definition node"""
        try:
            return {
                'name': self._get_function_name(node),
                'line': node.start_point[0] + 1,
                'end_line': node.end_point[0] + 1,
                'return_type': self._get_return_type(node)
            }
        except Exception as e:
            logger.debug(f"Error parsing function node: {e}")
            return None
    
    def _parse_class_node(self, node) -> Optional[Dict[str, Any]]:
        """Parse a class definition node"""
        try:
            return {
                'name': self._get_class_name(node),
                'line': node.start_point[0] + 1,
                'end_line': node.end_point[0] + 1,
                'type': 'class' if node.type == 'class_specifier' else 'struct'
            }
        except Exception as e:
            logger.debug(f"Error parsing class node: {e}")
            return None
    
    def _parse_include_node(self, node) -> Optional[Dict[str, Any]]:
        """Parse an include directive node"""
        try:
            text = self._get_node_text(node)
            return {
                'file': text,
                'line': node.start_point[0] + 1
            }
        except Exception as e:
            logger.debug(f"Error parsing include node: {e}")
            return None
    
    def _parse_variable_node(self, node) -> List[Dict[str, Any]]:
        """Parse variable declaration nodes"""
        variables = []
        try:
            for child in node.children:
                if child.type == 'init_declarator':
                    variables.append({
                        'name': self._get_node_text(child),
                        'line': child.start_point[0] + 1
                    })
        except Exception as e:
            logger.debug(f"Error parsing variable node: {e}")
        return variables
    
    def _get_node_text(self, node) -> str:
        """Get the text content of a node"""
        return self.source_code[node.start_byte:node.end_byte]
    
    def _get_function_name(self, node) -> str:
        """Extract function name from function definition node"""
        for child in node.children:
            if child.type == 'function_declarator':
                for subchild in child.children:
                    if subchild.type == 'identifier':
                        return self._get_node_text(subchild)
        return "unknown"
    
    def _get_class_name(self, node) -> str:
        """Extract class name from class definition node"""
        for child in node.children:
            if child.type == 'type_identifier':
                return self._get_node_text(child)
        return "unknown"
    
    def _get_return_type(self, node) -> str:
        """Extract return type from function definition node"""
        for child in node.children:
            if child.type in ('primitive_type', 'type_identifier'):
                return self._get_node_text(child)
        return "void"

# Made with Bob
