"""
Bug Explainer
Converts technical error messages into plain-language explanations
"""

from typing import Dict, List, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BugExplainer:
    """
    Provides plain-language explanations for bugs and errors
    """
    
    def __init__(self):
        """Initialize the bug explainer"""
        self.error_templates = self._load_error_templates()
    
    def explain(self, syntax_errors: List[Dict[str, Any]], 
               logic_errors: List[Dict[str, Any]],
               root_causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate plain-language explanations for errors
        
        Args:
            syntax_errors: List of syntax errors
            logic_errors: List of logic errors
            root_causes: List of root causes
            
        Returns:
            List of explanations
        """
        logger.info("Generating plain-language explanations")
        
        explanations = []
        
        # Explain syntax errors
        for error in syntax_errors:
            explanation = self._explain_syntax_error(error)
            if explanation:
                explanations.append(explanation)
        
        # Explain logic errors
        for error in logic_errors:
            explanation = self._explain_logic_error(error)
            if explanation:
                explanations.append(explanation)
        
        # Limit to top 5 most important explanations
        return explanations[:5]
    
    def _explain_syntax_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explain a syntax error in plain language
        
        Args:
            error: Syntax error details
            
        Returns:
            Plain-language explanation
        """
        message = error.get('message', '').lower()
        
        # Match error patterns and provide explanations
        if 'invalid syntax' in message:
            return self._create_explanation(
                error_type='SyntaxError',
                plain_explanation='There is a syntax error in your code. This means Python cannot understand what you wrote.',
                why_it_happens='Syntax errors occur when code does not follow the language rules, like missing colons, parentheses, or quotes.',
                how_to_fix='Check line {} for missing punctuation, incorrect indentation, or typos.'.format(error.get('line', 0)),
                code_example=self._suggest_fix_for_syntax(error)
            )
        
        elif 'unexpected eof' in message or 'eof' in message:
            return self._create_explanation(
                error_type='SyntaxError: Unexpected EOF',
                plain_explanation='Python reached the end of your file but expected more code.',
                why_it_happens='This usually means you have an unclosed bracket, parenthesis, or quote somewhere in your code.',
                how_to_fix='Look for opening brackets, parentheses, or quotes that are not closed. Check all your function definitions and loops.',
                code_example='Make sure every ( has a ), every [ has a ], and every { has a }'
            )
        
        elif 'indentation' in message:
            return self._create_explanation(
                error_type='IndentationError',
                plain_explanation='Your code indentation is incorrect.',
                why_it_happens='Python uses indentation (spaces or tabs) to understand code structure. Mixing tabs and spaces or incorrect indentation causes errors.',
                how_to_fix='Make sure all lines in the same block have the same indentation. Use either spaces or tabs consistently (4 spaces is recommended).',
                code_example='if condition:\n    do_something()  # 4 spaces\n    do_another()    # 4 spaces'
            )
        
        elif 'name' in message and 'not defined' in message:
            return self._create_explanation(
                error_type='NameError',
                plain_explanation='You are trying to use a variable or function that does not exist.',
                why_it_happens='This happens when you reference a variable before defining it, or when you have a typo in the name.',
                how_to_fix='Check the spelling of the variable/function name. Make sure you define it before using it.',
                code_example='# Define before use:\nx = 10\nprint(x)  # Correct'
            )
        
        elif 'missing' in message and 'parenthes' in message:
            return self._create_explanation(
                error_type='SyntaxError: Missing Parenthesis',
                plain_explanation='You forgot to close a parenthesis.',
                why_it_happens='Every opening parenthesis ( must have a matching closing parenthesis ).',
                how_to_fix='Count your parentheses on line {} and make sure they match.'.format(error.get('line', 0)),
                code_example='result = calculate(a, b)  # Both ( and ) are present'
            )
        
        # Default explanation for unknown syntax errors
        return self._create_explanation(
            error_type='Syntax Error',
            plain_explanation='There is an error in your code syntax at line {}.'.format(error.get('line', 0)),
            why_it_happens='The code does not follow the language rules.',
            how_to_fix='Review line {} carefully for typos, missing punctuation, or incorrect structure.'.format(error.get('line', 0)),
            code_example=error.get('code_snippet', '')
        )
    
    def _explain_logic_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explain a logic error in plain language
        
        Args:
            error: Logic error details
            
        Returns:
            Plain-language explanation
        """
        error_type = error.get('type', '').lower()
        
        if 'infinite_loop' in error_type:
            return self._create_explanation(
                error_type='Potential Infinite Loop',
                plain_explanation='Your loop might run forever without stopping.',
                why_it_happens='This happens when the loop condition never becomes false, so the loop keeps repeating.',
                how_to_fix='Make sure your loop has a condition that will eventually become false. Update the loop variable inside the loop.',
                code_example='# Good loop:\ni = 0\nwhile i < 10:\n    print(i)\n    i += 1  # This makes the loop end'
            )
        
        elif 'null_pointer' in error_type or 'none' in error_type:
            return self._create_explanation(
                error_type='Null/None Reference',
                plain_explanation='You are trying to use a variable that has no value (None/null).',
                why_it_happens='This happens when a variable is None/null and you try to access its properties or methods.',
                how_to_fix='Check if the variable is None before using it, or make sure it is properly initialized.',
                code_example='if my_var is not None:\n    my_var.do_something()'
            )
        
        elif 'type_mismatch' in error_type:
            return self._create_explanation(
                error_type='Type Mismatch',
                plain_explanation='You are trying to use a value of the wrong type.',
                why_it_happens='For example, trying to add a number to a string, or using a string where a number is expected.',
                how_to_fix='Make sure you are using the correct data types. Convert types if needed.',
                code_example='# Convert string to int:\nage = int("25")\nprint(age + 5)  # Now this works'
            )
        
        # Default logic error explanation
        return self._create_explanation(
            error_type='Logic Error',
            plain_explanation=error.get('message', 'There is a logic error in your code.'),
            why_it_happens='The code runs but does not produce the expected result.',
            how_to_fix=error.get('suggestion', 'Review the logic at line {}'.format(error.get('line', 0))),
            code_example=''
        )
    
    def _create_explanation(self, error_type: str, plain_explanation: str,
                          why_it_happens: str, how_to_fix: str,
                          code_example: str = '') -> Dict[str, Any]:
        """
        Create a structured explanation
        
        Args:
            error_type: Type of error
            plain_explanation: Simple explanation
            why_it_happens: Why this error occurs
            how_to_fix: How to fix it
            code_example: Example code
            
        Returns:
            Structured explanation dictionary
        """
        return {
            'error_type': error_type,
            'plain_explanation': plain_explanation,
            'why_it_happens': why_it_happens,
            'how_to_fix': how_to_fix,
            'code_example': code_example if code_example else None
        }
    
    def _suggest_fix_for_syntax(self, error: Dict[str, Any]) -> str:
        """Suggest a fix for a syntax error"""
        # Simplified - would analyze the actual error in detail
        return 'Check the syntax at line {}'.format(error.get('line', 0))
    
    def _load_error_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Load error explanation templates
        
        Returns:
            Dictionary of error templates
        """
        return {
            'syntax_error': {
                'title': 'Syntax Error',
                'description': 'The code does not follow language rules'
            },
            'indentation_error': {
                'title': 'Indentation Error',
                'description': 'Incorrect spacing at the beginning of lines'
            },
            'name_error': {
                'title': 'Name Error',
                'description': 'Using a variable that does not exist'
            },
            'type_error': {
                'title': 'Type Error',
                'description': 'Using the wrong type of data'
            },
            'infinite_loop': {
                'title': 'Infinite Loop',
                'description': 'A loop that never ends'
            }
        }

# Made with Bob
