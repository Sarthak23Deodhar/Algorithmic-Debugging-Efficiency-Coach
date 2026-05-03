"""
Debugging Engine Service - FastAPI Application
Main entry point for the debugging analysis service
"""

import time
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models.request import CodeSubmission
from .models.response import (
    DebugReport,
    ExecutionFlow,
    SyntaxError as SyntaxErrorModel,
    LogicError as LogicErrorModel,
    RootCause as RootCauseModel,
    Explanation as ExplanationModel
)
from .services.execution_flow import ExecutionFlowAnalyzer
from .services.root_cause import RootCauseIdentifier
from .services.explainer import BugExplainer
from .parsers import PythonParser, CppParser, JavaParser
from .utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Debugging Engine Service",
    description="Analyzes code submissions, diagnoses bugs, and provides plain-language explanations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
execution_flow_analyzer = ExecutionFlowAnalyzer()
root_cause_identifier = RootCauseIdentifier()
bug_explainer = BugExplainer()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status of the service
    """
    return {
        "status": "healthy",
        "service": "debugging-engine",
        "version": "1.0.0"
    }


@app.post("/api/v1/debug", response_model=DebugReport, status_code=status.HTTP_200_OK)
async def debug_code(submission: CodeSubmission):
    """
    Analyze code submission and provide debugging report
    
    Args:
        submission: Code submission with language and code
        
    Returns:
        Comprehensive debugging report
        
    Raises:
        HTTPException: If analysis fails
    """
    start_time = time.time()
    
    logger.info(f"Received debug request for {submission.language} code")
    
    try:
        # Step 1: Parse the code
        logger.info("Step 1: Parsing code")
        parsed_data = await _parse_code(submission.code, submission.language)
        
        # Step 2: Analyze execution flow
        logger.info("Step 2: Analyzing execution flow")
        execution_flow_data = execution_flow_analyzer.analyze(
            submission.code, 
            submission.language
        )
        
        # Step 3: Identify root causes
        logger.info("Step 3: Identifying root causes")
        root_cause_data = root_cause_identifier.identify(
            submission.code,
            submission.language,
            parsed_data
        )
        
        # Step 4: Generate explanations
        logger.info("Step 4: Generating explanations")
        explanations = bug_explainer.explain(
            root_cause_data.get('syntax_errors', []),
            root_cause_data.get('logic_errors', []),
            root_cause_data.get('root_causes', [])
        )
        
        # Calculate analysis time
        analysis_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Build response
        has_errors = (
            len(root_cause_data.get('syntax_errors', [])) > 0 or
            len(root_cause_data.get('logic_errors', [])) > 0
        )
        
        # Create ExecutionFlow object
        exec_flow = ExecutionFlow(
            entry_point=execution_flow_data.get('entry_point'),
            functions=execution_flow_data.get('functions', []),
            control_structures=execution_flow_data.get('control_structures', []),
            call_graph=execution_flow_data.get('call_graph', {}),
            unreachable_code=execution_flow_data.get('unreachable_code', [])
        )
        
        # Convert dictionaries to Pydantic models
        syntax_error_models = [SyntaxErrorModel(**err) for err in root_cause_data.get('syntax_errors', [])]
        logic_error_models = [LogicErrorModel(**err) for err in root_cause_data.get('logic_errors', [])]
        root_cause_models = [RootCauseModel(**rc) for rc in root_cause_data.get('root_causes', [])]
        explanation_models = [ExplanationModel(**exp) for exp in explanations]
        
        report = DebugReport(
            has_errors=has_errors,
            syntax_errors=syntax_error_models,
            logic_errors=logic_error_models,
            execution_flow=exec_flow,
            root_causes=root_cause_models,
            explanations=explanation_models,
            analysis_time_ms=analysis_time
        )
        
        logger.info(f"Analysis completed in {analysis_time:.2f}ms")
        return report
        
    except Exception as e:
        logger.error(f"Error during code analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze code: {str(e)}"
        )


async def _parse_code(code: str, language) -> dict:
    """
    Parse code using appropriate parser
    
    Args:
        code: Source code
        language: Programming language
        
    Returns:
        Parsed code structure
    """
    from .models.request import ProgrammingLanguage
    
    if language == ProgrammingLanguage.PYTHON:
        parser = PythonParser()
    elif language == ProgrammingLanguage.CPP:
        parser = CppParser()
    elif language == ProgrammingLanguage.JAVA:
        parser = JavaParser()
    else:
        raise ValueError(f"Unsupported language: {language}")
    
    return parser.parse(code)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )

# Made with Bob
