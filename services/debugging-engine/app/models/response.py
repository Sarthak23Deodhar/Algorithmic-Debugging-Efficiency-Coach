"""
Response models for the Debugging Engine API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SyntaxError(BaseModel):
    """
    Model for syntax errors
    
    Attributes:
        line: Line number where the error occurs
        column: Column number where the error occurs
        message: Error message
        code_snippet: Code snippet showing the error context
    """
    line: int = Field(..., description="Line number of the error")
    column: Optional[int] = Field(None, description="Column number of the error")
    message: str = Field(..., description="Error message")
    code_snippet: Optional[str] = Field(None, description="Code snippet with error context")
    severity: str = Field(default="error", description="Severity level: error, warning")


class LogicError(BaseModel):
    """
    Model for logic errors
    
    Attributes:
        type: Type of logic error (e.g., infinite_loop, null_pointer, type_mismatch)
        line: Line number where the error occurs
        message: Description of the logic error
        suggestion: Suggested fix
    """
    type: str = Field(..., description="Type of logic error")
    line: int = Field(..., description="Line number of the error")
    message: str = Field(..., description="Description of the logic error")
    suggestion: Optional[str] = Field(None, description="Suggested fix")
    severity: str = Field(default="warning", description="Severity level")


class ExecutionFlow(BaseModel):
    """
    Model for execution flow analysis
    
    Attributes:
        entry_point: Entry point of the program
        functions: List of functions found in the code
        control_structures: Control structures (loops, conditionals)
        call_graph: Function call relationships
        unreachable_code: List of unreachable code blocks
    """
    entry_point: Optional[str] = Field(None, description="Entry point of the program")
    functions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of functions with their metadata"
    )
    control_structures: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Control structures found in the code"
    )
    call_graph: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Function call relationships"
    )
    unreachable_code: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Unreachable code blocks"
    )


class RootCause(BaseModel):
    """
    Model for root cause analysis
    
    Attributes:
        issue_type: Type of issue (syntax, logic, memory, runtime)
        description: Detailed description of the root cause
        affected_lines: Lines affected by this issue
        confidence: Confidence score (0-1)
    """
    issue_type: str = Field(..., description="Type of issue")
    description: str = Field(..., description="Detailed description")
    affected_lines: List[int] = Field(..., description="Lines affected by this issue")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class Explanation(BaseModel):
    """
    Model for plain-language explanations
    
    Attributes:
        error_type: Type of error being explained
        plain_explanation: Beginner-friendly explanation
        why_it_happens: Why this error occurs
        how_to_fix: Step-by-step fix instructions
        code_example: Example of corrected code
    """
    error_type: str = Field(..., description="Type of error")
    plain_explanation: str = Field(..., description="Beginner-friendly explanation")
    why_it_happens: str = Field(..., description="Why this error occurs")
    how_to_fix: str = Field(..., description="How to fix the error")
    code_example: Optional[str] = Field(None, description="Example of corrected code")


class DebugReport(BaseModel):
    """
    Complete debugging report
    
    Attributes:
        has_errors: Whether any errors were found
        syntax_errors: List of syntax errors
        logic_errors: List of logic errors
        execution_flow: Execution flow analysis
        root_causes: Root cause analysis results
        explanations: Plain-language explanations
        analysis_time_ms: Time taken for analysis in milliseconds
    """
    has_errors: bool = Field(..., description="Whether any errors were found")
    syntax_errors: List[SyntaxError] = Field(
        default_factory=list,
        description="List of syntax errors"
    )
    logic_errors: List[LogicError] = Field(
        default_factory=list,
        description="List of logic errors"
    )
    execution_flow: Optional[ExecutionFlow] = Field(
        None,
        description="Execution flow analysis"
    )
    root_causes: List[RootCause] = Field(
        default_factory=list,
        description="Root cause analysis"
    )
    explanations: List[Explanation] = Field(
        default_factory=list,
        description="Plain-language explanations"
    )
    analysis_time_ms: Optional[float] = Field(
        None,
        description="Time taken for analysis in milliseconds"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "has_errors": True,
                "syntax_errors": [
                    {
                        "line": 5,
                        "column": 10,
                        "message": "SyntaxError: invalid syntax",
                        "code_snippet": "    return n * factorial(n-1",
                        "severity": "error"
                    }
                ],
                "logic_errors": [],
                "execution_flow": {
                    "entry_point": "factorial",
                    "functions": [{"name": "factorial", "line": 1, "params": ["n"]}],
                    "control_structures": [{"type": "if", "line": 2}],
                    "call_graph": {"factorial": ["factorial"]},
                    "unreachable_code": []
                },
                "root_causes": [
                    {
                        "issue_type": "syntax",
                        "description": "Missing closing parenthesis",
                        "affected_lines": [5],
                        "confidence": 0.95
                    }
                ],
                "explanations": [
                    {
                        "error_type": "SyntaxError",
                        "plain_explanation": "You forgot to close a parenthesis",
                        "why_it_happens": "Python requires all opening parentheses to be closed",
                        "how_to_fix": "Add a closing parenthesis at the end of line 5",
                        "code_example": "    return n * factorial(n-1)"
                    }
                ],
                "analysis_time_ms": 45.2
            }
        }

# Made with Bob
