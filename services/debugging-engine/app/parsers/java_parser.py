"""
Java code parser using tree-sitter
"""

from typing import Dict, List, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)

try:
    from tree_sitter import Language, Parser
    import tree_sitter_java as tsjava
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    logger.warning("tree-sitter not available, Java parsing will be limited")


class JavaParser:
    """
    Parser for Java code using tree-sitter
    """
    
    def __init__(self):
        """Initialize the Java parser"""
        self.parser: Optional[Any] = None
        self.tree: Optional[Any] = None
        self.source_code: str = ""
        
        if TREE_SITTER_AVAILABLE:
            try:
                JAVA_LANGUAGE = Language(tsjava.language())
                self.parser = Parser(JAVA_LANGUAGE)
            except Exception as e:
                logger.error(f"Failed to initialize Java parser: {e}")
                self.parser = None
    
    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse Java code and extract structural information
        
        Args:
            code: Java source code as string
            
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
                'functions': self._extract_methods(),
                'classes': self._extract_classes(),
                'imports': self._extract_imports(),
                'variables': self._extract_fields(),
                'control_structures': self._extract_control_structures(),
                'syntax_errors': self._check_syntax_errors()
            }
        except Exception as e:
            logger.error(f"Error parsing Java code: {e}")
            return {
                'success': False,
                'functions': [],
                'classes': [],
                'imports': [],
                'variables': [],
                'control_structures': [],
                'syntax_errors': [{'message': str(e), 'line': 0}]
            }
    
    def _fallback_parse(self, code: str) -> Dict[str, Any]:
        """Fallback parsing using simple regex patterns"""
        import re
        
        methods = []
        classes = []
        imports = []
        
        # Extract imports
        for match in re.finditer(r'import\s+([\w.]+);', code):
            imports.append({
                'package': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Extract class declarations
        for match in re.finditer(r'(?:public\s+)?class\s+(\w+)', code):
            classes.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Extract method declarations (simplified)
        for match in re.finditer(r'(?:public|private|protected)?\s*(?:static\s+)?(\w+)\s+(\w+)\s*\([^)]*\)\s*{', code):
            methods.append({
                'return_type': match.group(1),
                'name': match.group(2),
                'line': code[:match.start()].count('\n') + 1
            })
        
        return {
            'success': True,
            'functions': methods,
            'classes': classes,
            'imports': imports,
            'variables': [],
            'control_structures': [],
            'syntax_errors': []
        }
    
    def _extract_methods(self) -> List[Dict[str, Any]]:
        """Extract method definitions from the parse tree"""
        if not self.tree:
            return []
        
        methods = []
        
        def traverse(node):
            if node.type == 'method_declaration':
                method_info = self._parse_method_node(node)
                if method_info:
                    methods.append(method_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return methods
    
    def _extract_classes(self) -> List[Dict[str, Any]]:
        """Extract class definitions from the parse tree"""
        if not self.tree:
            return []
        
        classes = []
        
        def traverse(node):
            if node.type in ('class_declaration', 'interface_declaration'):
                class_info = self._parse_class_node(node)
                if class_info:
                    classes.append(class_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return classes
    
    def _extract_imports(self) -> List[Dict[str, Any]]:
        """Extract import statements"""
        if not self.tree:
            return []
        
        imports = []
        
        def traverse(node):
            if node.type == 'import_declaration':
                import_info = self._parse_import_node(node)
                if import_info:
                    imports.append(import_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return imports
    
    def _extract_fields(self) -> List[Dict[str, Any]]:
        """Extract field declarations"""
        if not self.tree:
            return []
        
        fields = []
        
        def traverse(node):
            if node.type == 'field_declaration':
                field_info = self._parse_field_node(node)
                if field_info:
                    fields.extend(field_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(self.tree.root_node)
        return fields
    
    def _extract_control_structures(self) -> List[Dict[str, Any]]:
        """Extract control flow structures"""
        if not self.tree:
            return []
        
        structures = []
        
        def traverse(node):
            if node.type in ('if_statement', 'for_statement', 'while_statement',
                           'do_statement', 'switch_expression', 'enhanced_for_statement'):
                structures.append({
                    'type': node.type.replace('_statement', '').replace('_expression', ''),
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
    
    def _parse_method_node(self, node) -> Optional[Dict[str, Any]]:
        """Parse a method declaration node"""
        try:
            return {
                'name': self._get_method_name(node),
                'line': node.start_point[0] + 1,
                'end_line': node.end_point[0] + 1,
                'return_type': self._get_return_type(node),
                'modifiers': self._get_modifiers(node)
            }
        except Exception as e:
            logger.debug(f"Error parsing method node: {e}")
            return None
    
    def _parse_class_node(self, node) -> Optional[Dict[str, Any]]:
        """Parse a class declaration node"""
        try:
            return {
                'name': self._get_class_name(node),
                'line': node.start_point[0] + 1,
                'end_line': node.end_point[0] + 1,
                'type': 'interface' if node.type == 'interface_declaration' else 'class',
                'modifiers': self._get_modifiers(node)
            }
        except Exception as e:
            logger.debug(f"Error parsing class node: {e}")
            return None
    
    def _parse_import_node(self, node) -> Optional[Dict[str, Any]]:
        """Parse an import declaration node"""
        try:
            text = self._get_node_text(node)
            return {
                'package': text.replace('import', '').replace(';', '').strip(),
                'line': node.start_point[0] + 1
            }
        except Exception as e:
            logger.debug(f"Error parsing import node: {e}")
            return None
    
    def _parse_field_node(self, node) -> List[Dict[str, Any]]:
        """Parse field declaration nodes"""
        fields = []
        try:
            for child in node.children:
                if child.type == 'variable_declarator':
                    for subchild in child.children:
                        if subchild.type == 'identifier':
                            fields.append({
                                'name': self._get_node_text(subchild),
                                'line': child.start_point[0] + 1
                            })
        except Exception as e:
            logger.debug(f"Error parsing field node: {e}")
        return fields
    
    def _get_node_text(self, node) -> str:
        """Get the text content of a node"""
        return self.source_code[node.start_byte:node.end_byte]
    
    def _get_method_name(self, node) -> str:
        """Extract method name from method declaration node"""
        for child in node.children:
            if child.type == 'identifier':
                return self._get_node_text(child)
        return "unknown"
    
    def _get_class_name(self, node) -> str:
        """Extract class name from class declaration node"""
        for child in node.children:
            if child.type == 'identifier':
                return self._get_node_text(child)
        return "unknown"
    
    def _get_return_type(self, node) -> str:
        """Extract return type from method declaration node"""
        for child in node.children:
            if child.type in ('type_identifier', 'void_type', 'integral_type'):
                return self._get_node_text(child)
        return "void"
    
    def _get_modifiers(self, node) -> List[str]:
        """Extract modifiers from a declaration node"""
        modifiers = []
        for child in node.children:
            if child.type == 'modifiers':
                for modifier in child.children:
                    modifiers.append(self._get_node_text(modifier))
        return modifiers

# Made with Bob
