"""
Main Serverless Function Handler for watsonx Orchestrate Integration
"""

import os
import uuid
from typing import Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.utils.logger import get_logger
from app.models.request import WorkflowRequest, WorkflowType, WebhookRequest
from app.models.response import WorkflowResponse, HealthCheckResponse, ErrorResponse, WorkflowStatus
from app.services.orchestrate_client import OrchestrateClient
from app.services.documentation import DocumentationService
from app.services.ticketing import TicketingService
from app.services.learning_path import LearningPathService
from app.workflows.post_analysis import PostAnalysisWorkflow
from app.workflows.optimization import OptimizationWorkflow
from app.workflows.developer_growth import DeveloperGrowthWorkflow

logger = get_logger(__name__)

app = FastAPI(title="watsonx Orchestrate Integration", version="1.0.0")

# Job tracking
active_jobs: Dict[str, Dict[str, Any]] = {}

# Initialize services (mock mode by default)
orchestrate_client = OrchestrateClient(mock_mode=True)
doc_service = DocumentationService(mock_mode=True)
ticket_service = TicketingService(mock_mode=True)
learning_service = LearningPathService(mock_mode=True)

# Initialize workflows
post_analysis_workflow = PostAnalysisWorkflow(orchestrate_client, doc_service, ticket_service)
optimization_workflow = OptimizationWorkflow(orchestrate_client, doc_service, ticket_service)
developer_growth_workflow = DeveloperGrowthWorkflow(orchestrate_client, learning_service)


@app.get("/health")
async def health_check() -> HealthCheckResponse:
    """Health check endpoint."""
    async with orchestrate_client:
        health = await orchestrate_client.health_check()
    
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        orchestrate_connected=health.get("status") == "healthy",
        mock_mode=orchestrate_client.mock_mode,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/workflow/trigger")
async def trigger_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks) -> WorkflowResponse:
    """Trigger a workflow execution."""
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    logger.info(f"Triggering workflow: {request.workflow_type} (job_id={job_id})")
    
    # Store job info
    active_jobs[job_id] = {
        "workflow_type": request.workflow_type,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Execute workflow in background
    background_tasks.add_task(
        execute_workflow_async,
        request.workflow_type,
        request.analysis_results,
        request.developer_id,
        request.project_id,
        job_id
    )
    
    return WorkflowResponse(
        job_id=job_id,
        workflow_type=request.workflow_type.value,
        status=WorkflowStatus.PENDING,
        actions_completed=[],
        next_steps=["Workflow execution in progress"],
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )


@app.get("/workflow/status/{job_id}")
async def get_workflow_status(job_id: str) -> WorkflowResponse:
    """Get workflow execution status."""
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_info = active_jobs[job_id]
    
    return WorkflowResponse(
        job_id=job_id,
        workflow_type=job_info["workflow_type"],
        status=WorkflowStatus(job_info["status"]),
        actions_completed=job_info.get("actions_completed", []),
        next_steps=job_info.get("next_steps", []),
        created_at=job_info["created_at"],
        updated_at=job_info.get("updated_at", job_info["created_at"]),
        metadata=job_info.get("metadata")
    )


@app.post("/webhook")
async def handle_webhook(request: WebhookRequest) -> Dict[str, str]:
    """Handle webhook callbacks from external systems."""
    logger.info(f"Received webhook: {request.event_type} from {request.source}")
    
    # Process webhook based on event type
    if request.event_type == "ticket_created":
        logger.info(f"Ticket created: {request.payload.get('ticket_id')}")
    elif request.event_type == "ticket_updated":
        logger.info(f"Ticket updated: {request.payload.get('ticket_id')}")
    
    return {"status": "received", "message": "Webhook processed successfully"}


async def execute_workflow_async(
    workflow_type: WorkflowType,
    analysis_results: Dict[str, Any],
    developer_id: str,
    project_id: str,
    job_id: str
):
    """Execute workflow asynchronously."""
    try:
        active_jobs[job_id]["status"] = "in_progress"
        
        async with orchestrate_client:
            if workflow_type == WorkflowType.POST_ANALYSIS:
                result = await post_analysis_workflow.execute(analysis_results, developer_id, project_id, job_id)
            elif workflow_type == WorkflowType.OPTIMIZATION:
                result = await optimization_workflow.execute(analysis_results, developer_id, project_id, job_id)
            elif workflow_type == WorkflowType.DEVELOPER_GROWTH:
                result = await developer_growth_workflow.execute(analysis_results, developer_id, project_id, job_id)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        # Update job status
        active_jobs[job_id].update({
            "status": result.status.value,
            "actions_completed": [a.dict() for a in result.actions_completed],
            "next_steps": result.next_steps,
            "updated_at": datetime.utcnow().isoformat(),
            "metadata": result.metadata
        })
        
        logger.info(f"Workflow {job_id} completed with status: {result.status}")
        
    except Exception as e:
        logger.error(f"Workflow {job_id} failed: {str(e)}")
        active_jobs[job_id].update({
            "status": "failed",
            "error": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message=str(exc),
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Made with Bob
