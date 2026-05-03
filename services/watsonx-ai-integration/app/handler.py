"""
Main serverless function handler for watsonx.ai Integration service
FastAPI application with async support
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from .models.request import (
    CodeGenerationRequest,
    RefactoringRequest,
    ExplanationRequest,
    OperationType
)
from .models.response import (
    AIResponse,
    JobStatus,
    HealthResponse
)
from .services.watsonx_client import WatsonxClient
from .services.code_generator import CodeGeneratorService
from .services.refactoring import RefactoringService
from .services.explainer import ExplainerService
from .utils.logger import get_logger

logger = get_logger(__name__)

# Global service instances
watsonx_client: WatsonxClient = None
code_generator: CodeGeneratorService = None
refactoring_service: RefactoringService = None
explainer_service: ExplainerService = None

# Job storage (in production, use Redis or database)
jobs: Dict[str, AIResponse] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown
    """
    # Startup
    global watsonx_client, code_generator, refactoring_service, explainer_service
    
    logger.info("Initializing watsonx.ai Integration service...")
    
    # Check if we should use mock mode
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    logger.info(f"Mock mode: {mock_mode}")
    
    # Initialize services
    watsonx_client = WatsonxClient(mock_mode=mock_mode)
    code_generator = CodeGeneratorService(watsonx_client)
    refactoring_service = RefactoringService(watsonx_client)
    explainer_service = ExplainerService(watsonx_client)
    
    logger.info("watsonx.ai Integration service initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down watsonx.ai Integration service...")


# Create FastAPI app
app = FastAPI(
    title="watsonx.ai Integration Service",
    description="AI-powered code generation, refactoring, and explanation service",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        service="watsonx-ai-integration",
        version="1.0.0",
        watsonx_connected=watsonx_client.is_connected() if watsonx_client else False,
        mock_mode=watsonx_client.mock_mode if watsonx_client else True
    )


@app.post("/generate", response_model=AIResponse)
async def generate_code(
    request: CodeGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate optimized code from problem description
    
    Args:
        request: Code generation request
        background_tasks: FastAPI background tasks
        
    Returns:
        AI response with job ID and status
    """
    try:
        # Create job
        job_id = f"gen_{uuid.uuid4().hex[:12]}"
        logger.info(f"Creating code generation job: {job_id}")
        
        # Create initial job response
        job_response = AIResponse(
            job_id=job_id,
            status=JobStatus.PROCESSING,
            operation_type=OperationType.GENERATE.value,
            created_at=datetime.utcnow()
        )
        jobs[job_id] = job_response
        
        # Process synchronously for now (can be made async with webhooks)
        result = await code_generator.generate_code(request)
        
        if result["success"]:
            job_response.status = JobStatus.COMPLETED
            job_response.generated_code = result["generated_code"]
            job_response.confidence_score = result["confidence_score"]
            job_response.processing_time_ms = result["processing_time_ms"]
            job_response.model_used = result["model_used"]
            job_response.completed_at = datetime.utcnow()
        else:
            job_response.status = JobStatus.FAILED
            job_response.error_message = result.get("error", "Unknown error")
            job_response.processing_time_ms = result.get("processing_time_ms")
        
        jobs[job_id] = job_response
        
        # If webhook URL provided, send callback
        if request.webhook_url:
            background_tasks.add_task(send_webhook, request.webhook_url, job_response)
        
        return job_response
        
    except Exception as e:
        logger.error(f"Code generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/refactor", response_model=AIResponse)
async def refactor_code(
    request: RefactoringRequest,
    background_tasks: BackgroundTasks
):
    """
    Refactor and optimize code
    
    Args:
        request: Refactoring request
        background_tasks: FastAPI background tasks
        
    Returns:
        AI response with job ID and status
    """
    try:
        # Create job
        job_id = f"ref_{uuid.uuid4().hex[:12]}"
        logger.info(f"Creating code refactoring job: {job_id}")
        
        # Create initial job response
        job_response = AIResponse(
            job_id=job_id,
            status=JobStatus.PROCESSING,
            operation_type=OperationType.REFACTOR.value,
            created_at=datetime.utcnow()
        )
        jobs[job_id] = job_response
        
        # Process synchronously
        result = await refactoring_service.refactor_code(request)
        
        if result["success"]:
            job_response.status = JobStatus.COMPLETED
            job_response.refactored_code = result["refactored_code"]
            job_response.confidence_score = result["confidence_score"]
            job_response.processing_time_ms = result["processing_time_ms"]
            job_response.model_used = result["model_used"]
            job_response.completed_at = datetime.utcnow()
        else:
            job_response.status = JobStatus.FAILED
            job_response.error_message = result.get("error", "Unknown error")
            job_response.processing_time_ms = result.get("processing_time_ms")
        
        jobs[job_id] = job_response
        
        # If webhook URL provided, send callback
        if request.webhook_url:
            background_tasks.add_task(send_webhook, request.webhook_url, job_response)
        
        return job_response
        
    except Exception as e:
        logger.error(f"Code refactoring failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain", response_model=AIResponse)
async def explain_code(
    request: ExplanationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate comprehensive code explanation
    
    Args:
        request: Explanation request
        background_tasks: FastAPI background tasks
        
    Returns:
        AI response with job ID and status
    """
    try:
        # Create job
        job_id = f"exp_{uuid.uuid4().hex[:12]}"
        logger.info(f"Creating code explanation job: {job_id}")
        
        # Create initial job response
        job_response = AIResponse(
            job_id=job_id,
            status=JobStatus.PROCESSING,
            operation_type=OperationType.EXPLAIN.value,
            created_at=datetime.utcnow()
        )
        jobs[job_id] = job_response
        
        # Process synchronously
        result = await explainer_service.explain_code(request)
        
        if result["success"]:
            job_response.status = JobStatus.COMPLETED
            job_response.explanation = result["explanation"]
            job_response.confidence_score = result["confidence_score"]
            job_response.processing_time_ms = result["processing_time_ms"]
            job_response.model_used = result["model_used"]
            job_response.completed_at = datetime.utcnow()
        else:
            job_response.status = JobStatus.FAILED
            job_response.error_message = result.get("error", "Unknown error")
            job_response.processing_time_ms = result.get("processing_time_ms")
        
        jobs[job_id] = job_response
        
        # If webhook URL provided, send callback
        if request.webhook_url:
            background_tasks.add_task(send_webhook, request.webhook_url, job_response)
        
        return job_response
        
    except Exception as e:
        logger.error(f"Code explanation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}", response_model=AIResponse)
async def get_job_status(job_id: str):
    """
    Get status of a job
    
    Args:
        job_id: Job identifier
        
    Returns:
        Job status and results
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    return jobs[job_id]


@app.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """
    Cancel a running job
    
    Args:
        job_id: Job identifier
        
    Returns:
        Cancellation confirmation
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job = jobs[job_id]
    if job.status == JobStatus.PROCESSING:
        job.status = JobStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        jobs[job_id] = job
        return {"message": f"Job {job_id} cancelled", "job": job}
    else:
        return {"message": f"Job {job_id} is already {job.status.value}", "job": job}


async def send_webhook(webhook_url: str, response: AIResponse):
    """
    Send webhook callback with job results
    
    Args:
        webhook_url: Webhook URL to call
        response: Job response to send
    """
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                webhook_url,
                json=response.dict(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    logger.info(f"Webhook sent successfully to {webhook_url}")
                else:
                    logger.warning(f"Webhook failed with status {resp.status}")
    except Exception as e:
        logger.error(f"Failed to send webhook: {e}")


# For local development
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8003"))
    logger.info(f"Starting watsonx.ai Integration service on port {port}")
    
    uvicorn.run(
        "app.handler:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

# Made with Bob