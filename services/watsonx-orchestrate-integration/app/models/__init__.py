"""
Data models for watsonx Orchestrate Integration Service
"""

from .request import (
    WorkflowRequest,
    DocumentationUpdateRequest,
    TicketRequest,
    LearningPathRequest,
    WorkflowType
)
from .response import (
    WorkflowResponse,
    DocumentationUpdateResponse,
    TicketResponse,
    LearningPathResponse,
    WorkflowStatus
)

__all__ = [
    "WorkflowRequest",
    "DocumentationUpdateRequest",
    "TicketRequest",
    "LearningPathRequest",
    "WorkflowType",
    "WorkflowResponse",
    "DocumentationUpdateResponse",
    "TicketResponse",
    "LearningPathResponse",
    "WorkflowStatus"
]

# Made with Bob
