"""
Request models for watsonx Orchestrate Integration Service
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class WorkflowType(str, Enum):
    """Types of workflows supported"""
    POST_ANALYSIS = "post_analysis"
    OPTIMIZATION = "optimization"
    DEVELOPER_GROWTH = "developer_growth"


class Priority(str, Enum):
    """Priority levels for tickets"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WorkflowRequest(BaseModel):
    """Request to trigger a workflow"""
    workflow_type: WorkflowType = Field(..., description="Type of workflow to execute")
    analysis_results: Dict[str, Any] = Field(..., description="Results from analysis services")
    developer_id: str = Field(..., description="ID of the developer")
    project_id: str = Field(..., description="ID of the project")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "workflow_type": "post_analysis",
                "analysis_results": {
                    "complexity": {"time": "O(n^2)", "space": "O(n)"},
                    "issues": ["nested loops", "inefficient sorting"]
                },
                "developer_id": "dev123",
                "project_id": "proj456",
                "metadata": {"file_path": "src/main.py"}
            }
        }


class DocumentationUpdateRequest(BaseModel):
    """Request to update documentation"""
    file_path: str = Field(..., description="Path to the file to document")
    complexity_changes: Dict[str, Any] = Field(..., description="Complexity analysis changes")
    optimization_notes: List[str] = Field(default_factory=list, description="Notes about optimizations")
    performance_metrics: Optional[Dict[str, Any]] = Field(default=None, description="Performance metrics")
    format_type: str = Field(default="markdown", description="Documentation format (markdown, rst, jsdoc)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "src/algorithms/sort.py",
                "complexity_changes": {
                    "before": {"time": "O(n^2)", "space": "O(1)"},
                    "after": {"time": "O(n log n)", "space": "O(n)"}
                },
                "optimization_notes": [
                    "Replaced bubble sort with merge sort",
                    "Improved time complexity from O(n^2) to O(n log n)"
                ],
                "performance_metrics": {
                    "execution_time_improvement": "75%",
                    "memory_usage": "+20%"
                },
                "format_type": "markdown"
            }
        }


class TicketRequest(BaseModel):
    """Request to create a ticket"""
    title: str = Field(..., description="Ticket title")
    description: str = Field(..., description="Detailed ticket description")
    priority: Priority = Field(..., description="Ticket priority")
    labels: List[str] = Field(default_factory=list, description="Ticket labels")
    assignee: Optional[str] = Field(default=None, description="Assignee username")
    file_path: Optional[str] = Field(default=None, description="Related file path")
    line_numbers: Optional[List[int]] = Field(default=None, description="Related line numbers")
    analysis_link: Optional[str] = Field(default=None, description="Link to analysis report")
    estimated_effort: Optional[str] = Field(default=None, description="Estimated effort (e.g., '2h', '1d')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Refactor inefficient sorting algorithm",
                "description": "The current implementation uses bubble sort with O(n^2) complexity. Should be replaced with a more efficient algorithm.",
                "priority": "high",
                "labels": ["performance", "refactoring", "technical-debt"],
                "assignee": "john.doe",
                "file_path": "src/algorithms/sort.py",
                "line_numbers": [45, 46, 47, 48, 49],
                "analysis_link": "https://analysis.example.com/report/123",
                "estimated_effort": "4h"
            }
        }


class SkillGap(BaseModel):
    """Represents a skill gap identified for a developer"""
    category: str = Field(..., description="Category (algorithms, data_structures, patterns)")
    topic: str = Field(..., description="Specific topic (e.g., 'Dynamic Programming')")
    severity: str = Field(..., description="Severity level (critical, moderate, minor)")
    frequency: int = Field(..., description="Number of times this gap was observed")
    examples: List[str] = Field(default_factory=list, description="Example code snippets or scenarios")


class LearningPathRequest(BaseModel):
    """Request to generate a learning path"""
    developer_id: str = Field(..., description="ID of the developer")
    skill_gaps: List[SkillGap] = Field(..., description="Identified skill gaps")
    recommended_topics: List[str] = Field(default_factory=list, description="Recommended topics to learn")
    current_skill_level: Optional[str] = Field(default="intermediate", description="Current skill level")
    learning_goals: Optional[List[str]] = Field(default=None, description="Specific learning goals")
    time_commitment: Optional[str] = Field(default="5h/week", description="Available time per week")
    
    class Config:
        json_schema_extra = {
            "example": {
                "developer_id": "dev123",
                "skill_gaps": [
                    {
                        "category": "algorithms",
                        "topic": "Dynamic Programming",
                        "severity": "critical",
                        "frequency": 5,
                        "examples": ["fibonacci", "knapsack problem"]
                    },
                    {
                        "category": "data_structures",
                        "topic": "Graph Algorithms",
                        "severity": "moderate",
                        "frequency": 3,
                        "examples": ["shortest path", "cycle detection"]
                    }
                ],
                "recommended_topics": [
                    "Dynamic Programming",
                    "Graph Algorithms",
                    "Time Complexity Analysis"
                ],
                "current_skill_level": "intermediate",
                "learning_goals": [
                    "Master dynamic programming",
                    "Improve algorithm optimization skills"
                ],
                "time_commitment": "5h/week"
            }
        }


class WebhookRequest(BaseModel):
    """Request from external system webhook"""
    event_type: str = Field(..., description="Type of event")
    payload: Dict[str, Any] = Field(..., description="Event payload")
    source: str = Field(..., description="Source system (jira, github, etc.)")
    timestamp: str = Field(..., description="Event timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "ticket_created",
                "payload": {
                    "ticket_id": "PROJ-123",
                    "status": "open"
                },
                "source": "jira",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

# Made with Bob
