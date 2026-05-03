"""
Response models for watsonx Orchestrate Integration Service
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class WorkflowStatus(str, Enum):
    """Status of workflow execution"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class ActionStatus(BaseModel):
    """Status of an individual action within a workflow"""
    action_name: str = Field(..., description="Name of the action")
    status: str = Field(..., description="Status of the action")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Action result")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    timestamp: str = Field(..., description="Timestamp of action completion")


class WorkflowResponse(BaseModel):
    """Response from workflow execution"""
    job_id: str = Field(..., description="Unique job identifier")
    workflow_type: str = Field(..., description="Type of workflow executed")
    status: WorkflowStatus = Field(..., description="Overall workflow status")
    actions_completed: List[ActionStatus] = Field(default_factory=list, description="Completed actions")
    next_steps: List[str] = Field(default_factory=list, description="Recommended next steps")
    created_at: str = Field(..., description="Workflow creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "job_abc123",
                "workflow_type": "post_analysis",
                "status": "completed",
                "actions_completed": [
                    {
                        "action_name": "update_documentation",
                        "status": "success",
                        "result": {"files_updated": 2},
                        "timestamp": "2024-01-15T10:30:00Z"
                    },
                    {
                        "action_name": "create_tickets",
                        "status": "success",
                        "result": {"tickets_created": 3},
                        "timestamp": "2024-01-15T10:31:00Z"
                    }
                ],
                "next_steps": [
                    "Review created tickets",
                    "Assign tickets to team members"
                ],
                "created_at": "2024-01-15T10:29:00Z",
                "updated_at": "2024-01-15T10:31:00Z"
            }
        }


class DocumentationUpdateResponse(BaseModel):
    """Response from documentation update"""
    success: bool = Field(..., description="Whether update was successful")
    files_updated: List[str] = Field(default_factory=list, description="List of updated files")
    changes_made: List[str] = Field(default_factory=list, description="Description of changes")
    version: Optional[str] = Field(default=None, description="Documentation version")
    commit_hash: Optional[str] = Field(default=None, description="Git commit hash if applicable")
    preview_url: Optional[str] = Field(default=None, description="URL to preview changes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "files_updated": [
                    "docs/algorithms/sort.md",
                    "README.md"
                ],
                "changes_made": [
                    "Added complexity analysis section",
                    "Updated performance benchmarks",
                    "Added optimization notes"
                ],
                "version": "1.2.0",
                "commit_hash": "abc123def456",
                "preview_url": "https://docs.example.com/preview/abc123"
            }
        }


class TicketResponse(BaseModel):
    """Response from ticket creation"""
    success: bool = Field(..., description="Whether ticket was created successfully")
    ticket_id: str = Field(..., description="Created ticket ID")
    ticket_url: str = Field(..., description="URL to view the ticket")
    assignee: Optional[str] = Field(default=None, description="Assigned user")
    priority: str = Field(..., description="Ticket priority")
    labels: List[str] = Field(default_factory=list, description="Applied labels")
    estimated_effort: Optional[str] = Field(default=None, description="Estimated effort")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "ticket_id": "PROJ-123",
                "ticket_url": "https://jira.example.com/browse/PROJ-123",
                "assignee": "john.doe",
                "priority": "high",
                "labels": ["performance", "refactoring", "technical-debt"],
                "estimated_effort": "4h"
            }
        }


class LearningResource(BaseModel):
    """A learning resource recommendation"""
    title: str = Field(..., description="Resource title")
    type: str = Field(..., description="Resource type (course, article, video, practice)")
    url: str = Field(..., description="Resource URL")
    difficulty: str = Field(..., description="Difficulty level")
    estimated_time: str = Field(..., description="Estimated time to complete")
    description: Optional[str] = Field(default=None, description="Resource description")


class LearningModule(BaseModel):
    """A module in the learning path"""
    module_name: str = Field(..., description="Module name")
    topics: List[str] = Field(..., description="Topics covered")
    resources: List[LearningResource] = Field(..., description="Learning resources")
    estimated_duration: str = Field(..., description="Estimated duration")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites")
    learning_objectives: List[str] = Field(default_factory=list, description="Learning objectives")


class LearningPathResponse(BaseModel):
    """Response from learning path generation"""
    success: bool = Field(..., description="Whether path was generated successfully")
    developer_id: str = Field(..., description="Developer ID")
    path_id: str = Field(..., description="Learning path ID")
    modules: List[LearningModule] = Field(..., description="Learning modules")
    total_estimated_time: str = Field(..., description="Total estimated time")
    skill_gaps_addressed: List[str] = Field(..., description="Skill gaps being addressed")
    progress_tracking_url: Optional[str] = Field(default=None, description="URL to track progress")
    next_assessment_date: Optional[str] = Field(default=None, description="Next assessment date")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "developer_id": "dev123",
                "path_id": "path_xyz789",
                "modules": [
                    {
                        "module_name": "Dynamic Programming Fundamentals",
                        "topics": ["Memoization", "Tabulation", "Common DP Patterns"],
                        "resources": [
                            {
                                "title": "Dynamic Programming - Introduction",
                                "type": "course",
                                "url": "https://example.com/dp-intro",
                                "difficulty": "intermediate",
                                "estimated_time": "4h",
                                "description": "Comprehensive introduction to DP"
                            }
                        ],
                        "estimated_duration": "2 weeks",
                        "prerequisites": ["Basic recursion"],
                        "learning_objectives": [
                            "Understand memoization and tabulation",
                            "Solve classic DP problems"
                        ]
                    }
                ],
                "total_estimated_time": "6 weeks",
                "skill_gaps_addressed": [
                    "Dynamic Programming",
                    "Algorithm Optimization"
                ],
                "progress_tracking_url": "https://learning.example.com/path/xyz789",
                "next_assessment_date": "2024-02-15"
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    orchestrate_connected: bool = Field(..., description="watsonx Orchestrate connection status")
    mock_mode: bool = Field(..., description="Whether running in mock mode")
    timestamp: str = Field(..., description="Current timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "orchestrate_connected": True,
                "mock_mode": False,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "WorkflowExecutionError",
                "message": "Failed to execute post_analysis workflow",
                "details": {
                    "failed_action": "create_tickets",
                    "reason": "API rate limit exceeded"
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

# Made with Bob
