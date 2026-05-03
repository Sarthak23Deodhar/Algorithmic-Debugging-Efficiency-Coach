"""
Learning Path Service

Generates personalized learning paths based on developer skill gaps.
"""

import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.utils.logger import get_logger
from app.models.request import LearningPathRequest, SkillGap
from app.models.response import LearningPathResponse, LearningModule, LearningResource

logger = get_logger(__name__)


class LearningPathService:
    """Service for generating personalized learning paths for developers."""
    
    RESOURCE_DATABASE = {
        "Dynamic Programming": [
            {"title": "DP Introduction", "type": "course", "url": "https://coursera.org/dp", "difficulty": "intermediate", "estimated_time": "4h", "description": "DP concepts"},
            {"title": "DP Practice", "type": "practice", "url": "https://leetcode.com/tag/dp", "difficulty": "intermediate", "estimated_time": "20h", "description": "DP problems"}
        ],
        "Graph Algorithms": [
            {"title": "Graph Theory", "type": "course", "url": "https://coursera.org/graphs", "difficulty": "intermediate", "estimated_time": "6h", "description": "Graph course"},
            {"title": "Graph Practice", "type": "practice", "url": "https://leetcode.com/tag/graph", "difficulty": "intermediate", "estimated_time": "15h", "description": "Graph problems"}
        ]
    }
    
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode or os.getenv("LEARNING_PATH_MOCK_MODE", "true").lower() == "true"
        self.generated_paths: List[Dict[str, Any]] = []
        logger.info(f"LearningPathService initialized (mock_mode={self.mock_mode})")
    
    async def generate_learning_path(self, request: LearningPathRequest) -> LearningPathResponse:
        logger.info(f"Generating learning path for developer: {request.developer_id}")
        try:
            prioritized_gaps = sorted(request.skill_gaps, key=lambda g: ({"critical": 3, "moderate": 2, "minor": 1}.get(g.severity, 0), g.frequency), reverse=True)
            modules = await self._generate_modules(prioritized_gaps, request.current_skill_level)
            total_time = f"{len(modules) * 2} weeks"
            path_id = f"path_{uuid.uuid4().hex[:12]}"
            next_assessment = (datetime.utcnow() + timedelta(weeks=len(modules) * 2)).strftime('%Y-%m-%d')
            
            self.generated_paths.append({"path_id": path_id, "developer_id": request.developer_id, "created_at": datetime.utcnow().isoformat()})
            
            return LearningPathResponse(
                success=True, developer_id=request.developer_id, path_id=path_id, modules=modules,
                total_estimated_time=total_time, skill_gaps_addressed=[g.topic for g in prioritized_gaps],
                progress_tracking_url=f"https://learning.example.com/path/{path_id}", next_assessment_date=next_assessment
            )
        except Exception as e:
            logger.error(f"Failed to generate learning path: {str(e)}")
            return LearningPathResponse(success=False, developer_id=request.developer_id, path_id="", modules=[], total_estimated_time="0h", skill_gaps_addressed=[])
    
    async def _generate_modules(self, skill_gaps: List[SkillGap], skill_level: str) -> List[LearningModule]:
        modules = []
        for gap in skill_gaps:
            raw_resources = self.RESOURCE_DATABASE.get(gap.topic, [])
            resources = [LearningResource(**r) for r in raw_resources]
            if resources:
                modules.append(LearningModule(
                    module_name=f"{gap.topic} Fundamentals",
                    topics=[gap.topic, "Practice", "Advanced Concepts"],
                    resources=resources,
                    estimated_duration="2 weeks",
                    prerequisites=["Basic programming"],
                    learning_objectives=[f"Master {gap.topic}", "Apply to real problems"]
                ))
        return modules

# Made with Bob
