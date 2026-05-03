"""Developer Growth Workflow - Triggered periodically or on-demand"""

from typing import Dict, Any, List
from datetime import datetime
from app.utils.logger import get_logger
from app.services.orchestrate_client import OrchestrateClient
from app.services.learning_path import LearningPathService
from app.models.request import LearningPathRequest, SkillGap
from app.models.response import WorkflowResponse, ActionStatus, WorkflowStatus

logger = get_logger(__name__)


class DeveloperGrowthWorkflow:
    """Workflow for developer skill assessment and learning path generation."""
    
    def __init__(self, orchestrate_client: OrchestrateClient, learning_service: LearningPathService):
        self.orchestrate = orchestrate_client
        self.learning_service = learning_service
        logger.info("DeveloperGrowthWorkflow initialized")
    
    async def execute(self, historical_data: Dict[str, Any], developer_id: str, project_id: str, job_id: str) -> WorkflowResponse:
        """Execute developer growth workflow."""
        logger.info(f"Executing developer growth workflow for {developer_id}")
        actions_completed = []
        
        try:
            # Action 1: Analyze historical submissions
            skill_gaps = self._analyze_submissions(historical_data.get("submissions", []))
            actions_completed.append(ActionStatus(
                action_name="analyze_submissions",
                status="success",
                result={"skill_gaps_identified": len(skill_gaps)},
                timestamp=datetime.utcnow().isoformat()
            ))
            
            # Action 2: Generate learning path
            learning_request = LearningPathRequest(
                developer_id=developer_id,
                skill_gaps=skill_gaps,
                recommended_topics=[gap.topic for gap in skill_gaps],
                current_skill_level=historical_data.get("skill_level", "intermediate")
            )
            learning_response = await self.learning_service.generate_learning_path(learning_request)
            actions_completed.append(ActionStatus(
                action_name="generate_learning_path",
                status="success" if learning_response.success else "failed",
                result={"path_id": learning_response.path_id, "modules": len(learning_response.modules)},
                timestamp=datetime.utcnow().isoformat()
            ))
            
            # Action 3: Schedule follow-up assessment
            actions_completed.append(ActionStatus(
                action_name="schedule_assessment",
                status="success",
                result={"next_assessment": learning_response.next_assessment_date},
                timestamp=datetime.utcnow().isoformat()
            ))
            
            return WorkflowResponse(
                job_id=job_id,
                workflow_type="developer_growth",
                status=WorkflowStatus.COMPLETED,
                actions_completed=actions_completed,
                next_steps=["Review learning path", "Start first module", "Track progress"],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                metadata={"learning_path_url": learning_response.progress_tracking_url}
            )
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return WorkflowResponse(
                job_id=job_id,
                workflow_type="developer_growth",
                status=WorkflowStatus.FAILED,
                actions_completed=actions_completed,
                next_steps=["Check error logs"],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
    
    def _analyze_submissions(self, submissions: List[Dict[str, Any]]) -> List[SkillGap]:
        """Analyze code submissions to identify skill gaps."""
        gap_tracker: Dict[str, Dict[str, Any]] = {}
        
        for submission in submissions:
            issues = submission.get("issues", [])
            for issue in issues:
                category = self._categorize_issue(issue)
                topic = self._extract_topic(issue)
                
                key = f"{category}:{topic}"
                if key not in gap_tracker:
                    gap_tracker[key] = {"category": category, "topic": topic, "frequency": 0, "examples": []}
                
                gap_tracker[key]["frequency"] += 1
                gap_tracker[key]["examples"].append(issue[:50])
        
        skill_gaps = []
        for gap_data in gap_tracker.values():
            severity = "critical" if gap_data["frequency"] >= 5 else "moderate" if gap_data["frequency"] >= 3 else "minor"
            skill_gaps.append(SkillGap(
                category=gap_data["category"],
                topic=gap_data["topic"],
                severity=severity,
                frequency=gap_data["frequency"],
                examples=gap_data["examples"][:3]
            ))
        
        return sorted(skill_gaps, key=lambda g: g.frequency, reverse=True)
    
    def _categorize_issue(self, issue: str) -> str:
        """Categorize an issue into algorithms, data_structures, or patterns."""
        issue_lower = issue.lower()
        if any(word in issue_lower for word in ["algorithm", "complexity", "optimization", "dynamic", "recursion"]):
            return "algorithms"
        elif any(word in issue_lower for word in ["array", "list", "tree", "graph", "hash", "heap"]):
            return "data_structures"
        else:
            return "patterns"
    
    def _extract_topic(self, issue: str) -> str:
        """Extract specific topic from issue description."""
        issue_lower = issue.lower()
        if "dynamic programming" in issue_lower or "dp" in issue_lower:
            return "Dynamic Programming"
        elif "graph" in issue_lower:
            return "Graph Algorithms"
        elif "complexity" in issue_lower:
            return "Time Complexity Analysis"
        else:
            return "Algorithm Optimization"

# Made with Bob
