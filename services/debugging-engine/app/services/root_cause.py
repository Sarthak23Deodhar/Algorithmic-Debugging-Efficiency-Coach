"""
Root Cause Identifier
Identifies syntax errors, logic errors, and potential issues in code
"""

import subprocess
import tempfile
import os
from typing import Dict, List, Any
from ..models.request import ProgrammingLanguage
from ..models.response import SyntaxError as SyntaxErrorModel, LogicError, RootCause
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RootCauseIdentifier:
    """
    Identifies root causes of bugs and errors in code
    """
    
    def __init__(self):
        """Initialize the root cause identifier"""
        pass
    
    def identify(self, code: str, language: ProgrammingLanguage, 
                parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify root causes of errors in the code
        
        Args:
            code: Source code to analyze
            language: Programming language
            parsed_data: Previously parsed code structure
            
        Returns:
            Dictionary containing identified issues
        """
        logger.info(f"Identifying root causes for {language} code")
        
        try:
            syntax_errors = self._check_syntax_errors(code, language, parsed_data)
            logic_errors = self._check_logic_errors(code, language, parsed_data)
            root_causes = self._analyze_root_causes(syntax_errors, logic_errors)
            
            return {
                'syntax_errors': syntax_errors,
                'logic_errors': logic_errors,
                'root_causes': root_causes
            }
            
        except Exception as e:
            logger.error(f"Error identifying root causes: {e}")
            return {
                'syntax_errors': [],
                'logic_errors': [],
                'root_causes': []
            }
    
    def _check_syntax_errors(self, code: str, language: ProgrammingLanguage,
                            parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check for syntax errors using language-specific tools
        
        Args:
            code: Source code
            language: Programming language
            parsed_data: Parsed code structure
            
        Returns:
            List of syntax errors
        """
        # First check if parser already found syntax errors
        parser_errors = parsed_data.get('syntax_errors', [])
        if parser_errors:
            return [self._format_syntax_error(err) for err in parser_errors]
        
        # Run language-specific linters
        if language == ProgrammingLanguage.PYTHON:
            return self._check_python_syntax(code)
        elif language == ProgrammingLanguage.CPP:
            return self._check_cpp_syntax(code)
        elif language == ProgrammingLanguage.JAVA:
            return self._check_java_syntax(code)
        
        return []
    
    def _check_python_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Check Python syntax using pylint"""
        errors = []
        
        try:
            # Write code to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run pylint
                result = subprocess.run(
                    ['pylint', '--errors-only', '--output-format=json', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.stdout:
                    import json
                    pylint_errors = json.loads(result.stdout)
                    for err in pylint_errors:
                        if err.get('type') in ('error', 'fatal'):
                            errors.append({
                                'line': err.get('line', 0),
                                'column': err.get('column', 0),
                                'message': err.get('message', ''),
                                'code_snippet': self._get_code_snippet(code, err.get('line', 0)),
                                'severity': 'error'
                            })
            finally:
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            logger.warning("Pylint timeout")
        except FileNotFoundError:
            logger.warning("Pylint not found, skipping syntax check")
        except Exception as e:
            logger.error(f"Error running pylint: {e}")
        
        return errors
    
    def _check_cpp_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Check C++ syntax using clang"""
        errors = []
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run clang with syntax-only check
                result = subprocess.run(
                    ['clang++', '-fsyntax-only', '-fno-color-diagnostics', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.stderr:
                    # Parse clang error output
                    for line in result.stderr.split('\n'):
                        if 'error:' in line:
                            errors.append(self._parse_clang_error(line, code))
            finally:
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            logger.warning("Clang timeout")
        except FileNotFoundError:
            logger.warning("Clang not found, skipping syntax check")
        except Exception as e:
            logger.error(f"Error running clang: {e}")
        
        return errors
    
    def _check_java_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Check Java syntax using javac"""
        errors = []
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run javac
                result = subprocess.run(
                    ['javac', '-Xdiags:verbose', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.stderr:
                    # Parse javac error output
                    for line in result.stderr.split('\n'):
                        if 'error:' in line:
                            errors.append(self._parse_javac_error(line, code))
            finally:
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            logger.warning("Javac timeout")
        except FileNotFoundError:
            logger.warning("Javac not found, skipping syntax check")
        except Exception as e:
            logger.error(f"Error running javac: {e}")
        
        return errors
    
    def _check_logic_errors(self, code: str, language: ProgrammingLanguage,
                           parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check for common logic errors
        
        Args:
            code: Source code
            language: Programming language
            parsed_data: Parsed code structure
            
        Returns:
            List of logic errors
        """
        logic_errors = []
        
        # Check for infinite loops
        logic_errors.extend(self._check_infinite_loops(parsed_data))
        
        # Check for unused variables
        logic_errors.extend(self._check_unused_variables(parsed_data))
        
        # Check for potential null pointer issues
        if language in (ProgrammingLanguage.CPP, ProgrammingLanguage.JAVA):
            logic_errors.extend(self._check_null_pointers(parsed_data))
        
        return logic_errors
    
    def _check_infinite_loops(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for potential infinite loops"""
        errors = []
        
        control_structures = parsed_data.get('control_structures', [])
        for struct in control_structures:
            if struct.get('type') == 'while':
                # Simplified check - would need more sophisticated analysis
                errors.append({
                    'type': 'potential_infinite_loop',
                    'line': struct.get('line', 0),
                    'message': 'Potential infinite loop detected',
                    'suggestion': 'Ensure loop has a proper exit condition',
                    'severity': 'warning'
                })
        
        return errors
    
    def _check_unused_variables(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for unused variables"""
        # Simplified implementation
        return []
    
    def _check_null_pointers(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for potential null pointer issues"""
        # Simplified implementation
        return []
    
    def _analyze_root_causes(self, syntax_errors: List[Dict[str, Any]], 
                            logic_errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze and categorize root causes
        
        Args:
            syntax_errors: List of syntax errors
            logic_errors: List of logic errors
            
        Returns:
            List of root causes with confidence scores
        """
        root_causes = []
        
        # Categorize syntax errors
        for error in syntax_errors:
            root_causes.append({
                'issue_type': 'syntax',
                'description': error.get('message', 'Syntax error'),
                'affected_lines': [error.get('line', 0)],
                'confidence': 0.95
            })
        
        # Categorize logic errors
        for error in logic_errors:
            root_causes.append({
                'issue_type': 'logic',
                'description': error.get('message', 'Logic error'),
                'affected_lines': [error.get('line', 0)],
                'confidence': 0.7
            })
        
        return root_causes
    
    def _format_syntax_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """Format a syntax error from parser"""
        return {
            'line': error.get('line', 0),
            'column': error.get('column', 0),
            'message': error.get('message', ''),
            'code_snippet': error.get('text', ''),
            'severity': 'error'
        }
    
    def _get_code_snippet(self, code: str, line: int, context: int = 2) -> str:
        """Get a code snippet around a specific line"""
        lines = code.split('\n')
        start = max(0, line - context - 1)
        end = min(len(lines), line + context)
        return '\n'.join(lines[start:end])
    
    def _parse_clang_error(self, error_line: str, code: str) -> Dict[str, Any]:
        """Parse clang error output"""
        # Simplified parsing
        return {
            'line': 0,
            'column': 0,
            'message': error_line,
            'code_snippet': '',
            'severity': 'error'
        }
    
    def _parse_javac_error(self, error_line: str, code: str) -> Dict[str, Any]:
        """Parse javac error output"""
        # Simplified parsing
        return {
            'line': 0,
            'column': 0,
            'message': error_line,
            'code_snippet': '',
            'severity': 'error'
        }

# Made with Bob
