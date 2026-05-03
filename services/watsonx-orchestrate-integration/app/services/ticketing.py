"""
Ticketing Service

Handles automated ticket creation in project tracking systems (Jira, GitHub Issues, etc.)
"""

import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.utils.logger import get_logger
from app.models.request import TicketRequest, Priority
from app.models.response import TicketResponse

logger = get_logger(__name__)


class TicketingService:
    """
    Service for creating and managing tickets in project tracking systems.
    
    Supports Jira, GitHub Issues, and other ticketing systems.
    """
    
    def __init__(
        self,
        system: str = "jira",
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
        project_key: Optional[str] = None,
        mock_mode: bool = True
    ):
        """
        Initialize the ticketing service.
        
        Args:
            system: Ticketing system (jira, github, etc.)
            api_url: API URL for the ticketing system
            api_token: API token for authentication
            project_key: Project key/identifier
            mock_mode: Whether to use mock mode (default: True)
        """
        self.system = system or os.getenv("TICKETING_SYSTEM", "jira")
        self.api_url = api_url or os.getenv("TICKETING_API_URL", "")
        self.api_token = api_token or os.getenv("TICKETING_API_TOKEN", "")
        self.project_key = project_key or os.getenv("TICKETING_PROJECT_KEY", "PROJ")
        self.mock_mode = mock_mode or os.getenv("TICKETING_MOCK_MODE", "true").lower() == "true"
        
        self.ticket_counter = 1000
        self.created_tickets: List[Dict[str, Any]] = []
        
        logger.info(f"TicketingService initialized (system={self.system}, mock_mode={self.mock_mode})")
    
    async def create_ticket(
        self,
        request: TicketRequest
    ) -> TicketResponse:
        """
        Create a ticket in the project tracking system.
        
        Args:
            request: Ticket creation request
            
        Returns:
            Ticket creation response
        """
        logger.info(f"Creating ticket: {request.title}")
        
        try:
            if self.system == "jira":
                return await self._create_jira_ticket(request)
            elif self.system == "github":
                return await self._create_github_ticket(request)
            else:
                return await self._create_generic_ticket(request)
                
        except Exception as e:
            logger.error(f"Failed to create ticket: {str(e)}")
            return TicketResponse(
                success=False,
                ticket_id="",
                ticket_url="",
                priority=request.priority.value,
                labels=request.labels
            )
    
    async def _create_jira_ticket(
        self,
        request: TicketRequest
    ) -> TicketResponse:
        """
        Create a Jira ticket.
        
        Args:
            request: Ticket creation request
            
        Returns:
            Ticket creation response
        """
        if self.mock_mode:
            return await self._create_mock_ticket(request, "jira")
        
        # Real Jira API integration would go here
        # from jira import JIRA
        # jira = JIRA(self.api_url, token_auth=self.api_token)
        # issue = jira.create_issue(...)
        
        logger.info("Real Jira integration not implemented, using mock")
        return await self._create_mock_ticket(request, "jira")
    
    async def _create_github_ticket(
        self,
        request: TicketRequest
    ) -> TicketResponse:
        """
        Create a GitHub issue.
        
        Args:
            request: Ticket creation request
            
        Returns:
            Ticket creation response
        """
        if self.mock_mode:
            return await self._create_mock_ticket(request, "github")
        
        # Real GitHub API integration would go here
        # from github import Github
        # g = Github(self.api_token)
        # repo = g.get_repo(self.project_key)
        # issue = repo.create_issue(...)
        
        logger.info("Real GitHub integration not implemented, using mock")
        return await self._create_mock_ticket(request, "github")
    
    async def _create_generic_ticket(
        self,
        request: TicketRequest
    ) -> TicketResponse:
        """
        Create a generic ticket (fallback).
        
        Args:
            request: Ticket creation request
            
        Returns:
            Ticket creation response
        """
        return await self._create_mock_ticket(request, "generic")
    
    async def _create_mock_ticket(
        self,
        request: TicketRequest,
        system: str
    ) -> TicketResponse:
        """
        Create a mock ticket for development.
        
        Args:
            request: Ticket creation request
            system: Ticketing system name
            
        Returns:
            Mock ticket response
        """
        self.ticket_counter += 1
        ticket_id = f"{self.project_key}-{self.ticket_counter}"
        
        # Generate ticket URL based on system
        if system == "jira":
            ticket_url = f"https://jira.example.com/browse/{ticket_id}"
        elif system == "github":
            ticket_url = f"https://github.com/example/repo/issues/{self.ticket_counter}"
        else:
            ticket_url = f"https://tickets.example.com/{ticket_id}"
        
        # Store ticket information
        ticket_info = {
            "ticket_id": ticket_id,
            "title": request.title,
            "description": request.description,
            "priority": request.priority.value,
            "labels": request.labels,
            "assignee": request.assignee,
            "file_path": request.file_path,
            "line_numbers": request.line_numbers,
            "analysis_link": request.analysis_link,
            "estimated_effort": request.estimated_effort,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open"
        }
        
        self.created_tickets.append(ticket_info)
        
        logger.info(f"[MOCK] Created {system} ticket: {ticket_id}")
        
        return TicketResponse(
            success=True,
            ticket_id=ticket_id,
            ticket_url=ticket_url,
            assignee=request.assignee,
            priority=request.priority.value,
            labels=request.labels,
            estimated_effort=request.estimated_effort
        )
    
    async def create_refactoring_ticket(
        self,
        file_path: str,
        issue_description: str,
        complexity_info: Dict[str, Any],
        priority: Priority = Priority.MEDIUM
    ) -> TicketResponse:
        """
        Create a refactoring ticket based on code analysis.
        
        Args:
            file_path: Path to the file needing refactoring
            issue_description: Description of the issue
            complexity_info: Complexity analysis information
            priority: Ticket priority
            
        Returns:
            Ticket creation response
        """
        # Generate ticket title
        title = f"Refactor: {issue_description} in {file_path}"
        
        # Generate detailed description
        description = self._generate_refactoring_description(
            file_path,
            issue_description,
            complexity_info
        )
        
        # Create ticket request
        request = TicketRequest(
            title=title,
            description=description,
            priority=priority,
            labels=["refactoring", "performance", "technical-debt"],
            file_path=file_path,
            estimated_effort=self._estimate_effort(complexity_info)
        )
        
        return await self.create_ticket(request)
    
    def _generate_refactoring_description(
        self,
        file_path: str,
        issue_description: str,
        complexity_info: Dict[str, Any]
    ) -> str:
        """
        Generate a detailed ticket description for refactoring.
        
        Args:
            file_path: File path
            issue_description: Issue description
            complexity_info: Complexity information
            
        Returns:
            Formatted ticket description
        """
        description = f"""## Issue Description
{issue_description}

## File Information
- **File**: `{file_path}`
- **Current Time Complexity**: {complexity_info.get('time_complexity', 'Unknown')}
- **Current Space Complexity**: {complexity_info.get('space_complexity', 'Unknown')}

## Analysis Details
"""
        
        if "issues" in complexity_info:
            description += "\n### Identified Issues\n"
            for issue in complexity_info["issues"]:
                description += f"- {issue}\n"
        
        if "suggestions" in complexity_info:
            description += "\n### Suggested Improvements\n"
            for suggestion in complexity_info["suggestions"]:
                description += f"- {suggestion}\n"
        
        description += """
## Acceptance Criteria
- [ ] Code refactored to improve complexity
- [ ] Unit tests updated/added
- [ ] Documentation updated
- [ ] Performance benchmarks show improvement

## Additional Notes
This ticket was automatically generated based on code analysis results.
"""
        
        return description
    
    def _estimate_effort(
        self,
        complexity_info: Dict[str, Any]
    ) -> str:
        """
        Estimate effort required for refactoring.
        
        Args:
            complexity_info: Complexity information
            
        Returns:
            Effort estimate (e.g., "2h", "1d")
        """
        # Simple heuristic based on complexity
        time_complexity = complexity_info.get('time_complexity', '')
        
        if 'n^3' in time_complexity or 'n^4' in time_complexity:
            return "1d"
        elif 'n^2' in time_complexity:
            return "4h"
        elif 'n log n' in time_complexity:
            return "2h"
        else:
            return "1h"
    
    async def bulk_create_tickets(
        self,
        issues: List[Dict[str, Any]]
    ) -> List[TicketResponse]:
        """
        Create multiple tickets in bulk.
        
        Args:
            issues: List of issue dictionaries
            
        Returns:
            List of ticket responses
        """
        logger.info(f"Creating {len(issues)} tickets in bulk")
        
        responses = []
        for issue in issues:
            request = TicketRequest(
                title=issue.get("title", "Untitled Issue"),
                description=issue.get("description", ""),
                priority=Priority(issue.get("priority", "medium")),
                labels=issue.get("labels", []),
                assignee=issue.get("assignee"),
                file_path=issue.get("file_path"),
                line_numbers=issue.get("line_numbers"),
                estimated_effort=issue.get("estimated_effort")
            )
            
            response = await self.create_ticket(request)
            responses.append(response)
        
        logger.info(f"Created {len(responses)} tickets")
        return responses
    
    def get_created_tickets(self) -> List[Dict[str, Any]]:
        """
        Get list of all created tickets.
        
        Returns:
            List of ticket information
        """
        return self.created_tickets
    
    def get_ticket_by_id(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Get ticket information by ID.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            Ticket information or None
        """
        for ticket in self.created_tickets:
            if ticket["ticket_id"] == ticket_id:
                return ticket
        return None
    
    async def update_ticket_status(
        self,
        ticket_id: str,
        status: str
    ) -> bool:
        """
        Update ticket status.
        
        Args:
            ticket_id: Ticket identifier
            status: New status
            
        Returns:
            Success status
        """
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            ticket["status"] = status
            ticket["updated_at"] = datetime.utcnow().isoformat()
            logger.info(f"Updated ticket {ticket_id} status to {status}")
            return True
        
        logger.warning(f"Ticket not found: {ticket_id}")
        return False

# Made with Bob
