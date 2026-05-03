"""Post-Analysis Workflow - Triggered after code analysis completes"""

from typing import Dict, Any
from datetime import datetime
from app.utils.logger import get_logger
from app.services.orchestrate_client import OrchestrateClient
from app.services.documentation import DocumentationService
from app.services.ticketing import TicketingService
from app.models.request import DocumentationUpdateRequest, Priority
from app.models.response import WorkflowResponse, ActionStatus, WorkflowStatus

logger = get_logger(__name__)


class PostAnalysisWorkflow:
    """Workflow triggered after code analysis completes."""
    
    def __init__(self, orchestrate_client: OrchestrateClient, doc_service: DocumentationService, ticket_service: TicketingService):
        self.orchestrate = orchestrate_client
        self.doc_service = doc_service
        self.ticket_service = ticket_service
        logger.info("PostAnalysisWorkflow initialized")
    
    async def execute(self, analysis_results: Dict[str, Any], developer_id: str, project_id: str, job_id: str) -> WorkflowResponse:
        """Execute post-analysis workflow."""
        logger.info(f"Executing post-analysis workflow for job {job_id}")
        actions_completed = []
        
        try:
            # Action 1: Update documentation
            if "file_path" in analysis_results:
                doc_request = DocumentationUpdateRequest(
                    file_path=analysis_results["file_path"],
                    complexity_changes=analysis_results.get("complexity", {}),
                    optimization_notes=analysis_results.get("suggestions", []),
                    performance_metrics=analysis_results.get("metrics", {})
                )
                doc_response = await self.doc_service.update_documentation(doc_request)
                actions_completed.append(ActionStatus(
                    action_name="update_documentation",
                    status="success" if doc_response.success else "failed",
                    result={"files_updated": len(doc_response.files_updated)},
                    timestamp=datetime.utcnow().isoformat()
                ))
            
            # Action 2: Create tickets for issues
            if "issues" in analysis_results:
                tickets_created = 0
                for issue in analysis_results["issues"][:3]:  # Limit to top 3
                    ticket_response = await self.ticket_service.create_refactoring_ticket(
                        file_path=analysis_results.get("file_path", "unknown"),
                        issue_description=issue,
                        complexity_info=analysis_results.get("complexity", {}),
                        priority=Priority.HIGH if "critical" in issue.lower() else Priority.MEDIUM
                    )
                    if ticket_response.success:
                        tickets_created += 1
                
                actions_completed.append(ActionStatus(
                    action_name="create_tickets",
                    status="success",
                    result={"tickets_created": tickets_created},
                    timestamp=datetime.utcnow().isoformat()
                ))
            
            # Action 3: Send notifications
            await self.orchestrate.send_notification(
                channel="email",
                message=f"Code analysis completed for {analysis_results.get('file_path', 'unknown')}",
                recipients=[developer_id]
            )
            actions_completed.append(ActionStatus(
                action_name="send_notifications",
                status="success",
                result={"recipients": 1},
                timestamp=datetime.utcnow().isoformat()
            ))
            
            return WorkflowResponse(
                job_id=job_id,
                workflow_type="post_analysis",
                status=WorkflowStatus.COMPLETED,
                actions_completed=actions_completed,
                next_steps=["Review created tickets", "Verify documentation updates"],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return WorkflowResponse(
                job_id=job_id,
                workflow_type="post_analysis",
                status=WorkflowStatus.FAILED,
                actions_completed=actions_completed,
                next_steps=["Check error logs", "Retry workflow"],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )

# Made with Bob
