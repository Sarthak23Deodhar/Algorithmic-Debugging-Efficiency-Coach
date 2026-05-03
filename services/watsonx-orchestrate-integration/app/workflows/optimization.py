"""Optimization Workflow - Triggered when optimization is applied"""

from typing import Dict, Any
from datetime import datetime
from app.utils.logger import get_logger
from app.services.orchestrate_client import OrchestrateClient
from app.services.documentation import DocumentationService
from app.services.ticketing import TicketingService
from app.models.request import DocumentationUpdateRequest
from app.models.response import WorkflowResponse, ActionStatus, WorkflowStatus

logger = get_logger(__name__)


class OptimizationWorkflow:
    """Workflow triggered when code optimization is applied."""
    
    def __init__(self, orchestrate_client: OrchestrateClient, doc_service: DocumentationService, ticket_service: TicketingService):
        self.orchestrate = orchestrate_client
        self.doc_service = doc_service
        self.ticket_service = ticket_service
        logger.info("OptimizationWorkflow initialized")
    
    async def execute(self, optimization_results: Dict[str, Any], developer_id: str, project_id: str, job_id: str) -> WorkflowResponse:
        """Execute optimization workflow."""
        logger.info(f"Executing optimization workflow for job {job_id}")
        actions_completed = []
        
        try:
            # Action 1: Update documentation with new complexity
            doc_request = DocumentationUpdateRequest(
                file_path=optimization_results.get("file_path", "unknown"),
                complexity_changes={
                    "before": optimization_results.get("before_complexity", {}),
                    "after": optimization_results.get("after_complexity", {})
                },
                optimization_notes=optimization_results.get("changes_made", []),
                performance_metrics=optimization_results.get("performance_improvement", {})
            )
            doc_response = await self.doc_service.update_documentation(doc_request)
            actions_completed.append(ActionStatus(
                action_name="update_documentation",
                status="success" if doc_response.success else "failed",
                result={"files_updated": len(doc_response.files_updated)},
                timestamp=datetime.utcnow().isoformat()
            ))
            
            # Action 2: Close related tickets
            if "related_ticket_ids" in optimization_results:
                for ticket_id in optimization_results["related_ticket_ids"]:
                    await self.ticket_service.update_ticket_status(ticket_id, "resolved")
                actions_completed.append(ActionStatus(
                    action_name="close_tickets",
                    status="success",
                    result={"tickets_closed": len(optimization_results["related_ticket_ids"])},
                    timestamp=datetime.utcnow().isoformat()
                ))
            
            # Action 3: Log performance improvements
            improvement_pct = optimization_results.get("performance_improvement", {}).get("percentage", 0)
            actions_completed.append(ActionStatus(
                action_name="log_improvements",
                status="success",
                result={"improvement_percentage": improvement_pct},
                timestamp=datetime.utcnow().isoformat()
            ))
            
            return WorkflowResponse(
                job_id=job_id,
                workflow_type="optimization",
                status=WorkflowStatus.COMPLETED,
                actions_completed=actions_completed,
                next_steps=["Verify performance improvements", "Update team on changes"],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return WorkflowResponse(
                job_id=job_id,
                workflow_type="optimization",
                status=WorkflowStatus.FAILED,
                actions_completed=actions_completed,
                next_steps=["Check error logs"],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )

# Made with Bob
