"""
Execution Flow Analyzer
Analyzes code execution paths and control flow
"""

from typing import Dict, List, Any, Optional
from ..models.request import ProgrammingLanguage
from ..parsers import PythonParser, CppParser, JavaParser
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionFlowAnalyzer:
    """
    Analyzes execution flow of code submissions
    """
    
    def __init__(self):
        """Initialize the execution flow analyzer"""
        self.python_parser = PythonParser()
        self.cpp_parser = CppParser()
        self.java_parser = JavaParser()
    
    def analyze(self, code: str, language: ProgrammingLanguage) -> Dict[str, Any]:
        """
        Analyze execution flow of the given code
        
        Args:
            code: Source code to analyze
            language: Programming language of the code
            
        Returns:
            Dictionary containing execution flow analysis
        """
        logger.info(f"Analyzing execution flow for {language} code")
        
        try:
            # Parse the code based on language
            if language == ProgrammingLanguage.PYTHON:
                parsed_data = self.python_parser.parse(code)
            elif language == ProgrammingLanguage.CPP:
                parsed_data = self.cpp_parser.parse(code)
            elif language == ProgrammingLanguage.JAVA:
                parsed_data = self.java_parser.parse(code)
            else:
                return self._empty_flow()
            
            if not parsed_data.get('success', False):
                logger.warning("Parsing failed, returning limited flow analysis")
                return self._empty_flow()
            
            # Build execution flow from parsed data
            flow = self._build_execution_flow(parsed_data, language)
            
            logger.info("Execution flow analysis completed")
            return flow
            
        except Exception as e:
            logger.error(f"Error analyzing execution flow: {e}")
            return self._empty_flow()
    
    def _build_execution_flow(self, parsed_data: Dict[str, Any], 
                             language: ProgrammingLanguage) -> Dict[str, Any]:
        """
        Build execution flow structure from parsed data
        
        Args:
            parsed_data: Parsed code structure
            language: Programming language
            
        Returns:
            Execution flow dictionary
        """
        functions = parsed_data.get('functions', [])
        classes = parsed_data.get('classes', [])
        control_structures = parsed_data.get('control_structures', [])
        
        # Determine entry point
        entry_point = self._find_entry_point(functions, classes, language)
        
        # Build call graph
        call_graph = self._build_call_graph(functions)
        
        # Identify unreachable code
        unreachable = self._find_unreachable_code(functions, control_structures)
        
        return {
            'entry_point': entry_point,
            'functions': functions,
            'control_structures': control_structures,
            'call_graph': call_graph,
            'unreachable_code': unreachable
        }
    
    def _find_entry_point(self, functions: List[Dict[str, Any]],
                         classes: List[Dict[str, Any]],
                         language: ProgrammingLanguage) -> Optional[str]:
        """
        Find the entry point of the program
        
        Args:
            functions: List of functions
            classes: List of classes
            language: Programming language
            
        Returns:
            Entry point name or None
        """
        if language == ProgrammingLanguage.PYTHON:
            # Look for if __name__ == "__main__" or top-level code
            return "module_level"
        
        elif language == ProgrammingLanguage.CPP:
            # Look for main function
            for func in functions:
                if func.get('name') == 'main':
                    return 'main'
            return None
        
        elif language == ProgrammingLanguage.JAVA:
            # Look for public static void main
            for func in functions:
                if func.get('name') == 'main':
                    modifiers = func.get('modifiers', [])
                    if 'public' in modifiers and 'static' in modifiers:
                        return 'main'
            return None
        
        return None
    
    def _build_call_graph(self, functions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Build a call graph showing function relationships
        
        Args:
            functions: List of functions
            
        Returns:
            Dictionary mapping function names to called functions
        """
        call_graph = {}
        
        # Simplified call graph - in a real implementation, 
        # we would analyze function bodies for calls
        for func in functions:
            func_name = func.get('name', 'unknown')
            call_graph[func_name] = []
        
        return call_graph
    
    def _find_unreachable_code(self, functions: List[Dict[str, Any]], 
                              control_structures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify potentially unreachable code blocks
        
        Args:
            functions: List of functions
            control_structures: List of control structures
            
        Returns:
            List of unreachable code blocks
        """
        unreachable = []
        
        # Simplified detection - would need more sophisticated analysis
        # Look for code after return statements, infinite loops, etc.
        
        return unreachable
    
    def _empty_flow(self) -> Dict[str, Any]:
        """Return an empty execution flow structure"""
        return {
            'entry_point': None,
            'functions': [],
            'control_structures': [],
            'call_graph': {},
            'unreachable_code': []
        }

# Made with Bob
