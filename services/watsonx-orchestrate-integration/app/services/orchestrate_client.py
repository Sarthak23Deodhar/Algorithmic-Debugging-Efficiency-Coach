"""
watsonx Orchestrate API Client

Handles communication with IBM watsonx Orchestrate for workflow automation.
Supports both real API mode and mock mode for development.
"""

import os
import asyncio
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
import aiohttp
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OrchestrateClient:
    """
    Client for interacting with IBM watsonx Orchestrate API.
    
    Supports mock mode for development without actual API credentials.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        mock_mode: bool = True
    ):
        """
        Initialize the Orchestrate client.
        
        Args:
            api_key: watsonx Orchestrate API key
            api_url: watsonx Orchestrate API URL
            mock_mode: Whether to use mock mode (default: True for development)
        """
        self.api_key = api_key or os.getenv("ORCHESTRATE_API_KEY", "")
        self.api_url = api_url or os.getenv("ORCHESTRATE_API_URL", "https://api.orchestrate.ibm.com")
        self.mock_mode = mock_mode or os.getenv("ORCHESTRATE_MOCK_MODE", "true").lower() == "true"
        
        if not self.mock_mode and not self.api_key:
            logger.warning("No API key provided, falling back to mock mode")
            self.mock_mode = True
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds
        
        logger.info(f"OrchestrateClient initialized (mock_mode={self.mock_mode})")
    
    async def __aenter__(self):
        """Async context manager entry."""
        if not self.mock_mode:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Make an API request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request payload
            retry_count: Current retry attempt
            
        Returns:
            API response data
            
        Raises:
            Exception: If request fails after all retries
        """
        if self.mock_mode:
            return await self._mock_request(method, endpoint, data)
        
        url = f"{self.api_url}/{endpoint}"
        
        try:
            async with self.session.request(method, url, json=data) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            if retry_count < self.max_retries:
                delay = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                logger.warning(f"Request failed, retrying in {delay}s... (attempt {retry_count + 1}/{self.max_retries})")
                await asyncio.sleep(delay)
                return await self._make_request(method, endpoint, data, retry_count + 1)
            else:
                logger.error(f"Request failed after {self.max_retries} retries: {str(e)}")
                raise
    
    async def _mock_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Mock API request for development.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            Mock response data
        """
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        logger.info(f"[MOCK] {method} /{endpoint}")
        if data:
            logger.debug(f"[MOCK] Request data: {data}")
        
        # Generate mock responses based on endpoint
        if "workflow" in endpoint:
            return {
                "job_id": f"mock_job_{uuid.uuid4().hex[:8]}",
                "status": "submitted",
                "message": "Workflow submitted successfully (mock)"
            }
        elif "skill" in endpoint:
            return {
                "skill_id": f"mock_skill_{uuid.uuid4().hex[:8]}",
                "status": "active",
                "message": "Skill configured successfully (mock)"
            }
        else:
            return {
                "status": "success",
                "message": "Operation completed successfully (mock)"
            }
    
    async def trigger_workflow(
        self,
        workflow_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger a workflow in watsonx Orchestrate.
        
        Args:
            workflow_name: Name of the workflow to trigger
            parameters: Workflow parameters
            
        Returns:
            Workflow execution details
        """
        logger.info(f"Triggering workflow: {workflow_name}")
        
        payload = {
            "workflow_name": workflow_name,
            "parameters": parameters,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = await self._make_request("POST", "workflows/trigger", payload)
        
        logger.info(f"Workflow triggered: {response.get('job_id', 'unknown')}")
        return response
    
    async def get_workflow_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow execution.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Workflow status details
        """
        logger.info(f"Getting workflow status: {job_id}")
        
        if self.mock_mode:
            return {
                "job_id": job_id,
                "status": "completed",
                "progress": 100,
                "result": {
                    "actions_completed": 3,
                    "actions_failed": 0
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        
        return await self._make_request("GET", f"workflows/status/{job_id}")
    
    async def configure_skill(
        self,
        skill_name: str,
        configuration: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Configure a skill in watsonx Orchestrate.
        
        Args:
            skill_name: Name of the skill
            configuration: Skill configuration
            
        Returns:
            Configuration result
        """
        logger.info(f"Configuring skill: {skill_name}")
        
        payload = {
            "skill_name": skill_name,
            "configuration": configuration,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = await self._make_request("POST", "skills/configure", payload)
        
        logger.info(f"Skill configured: {skill_name}")
        return response
    
    async def register_webhook(
        self,
        webhook_url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """
        Register a webhook for receiving events.
        
        Args:
            webhook_url: URL to receive webhook events
            events: List of event types to subscribe to
            
        Returns:
            Webhook registration details
        """
        logger.info(f"Registering webhook: {webhook_url}")
        
        payload = {
            "webhook_url": webhook_url,
            "events": events,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = await self._make_request("POST", "webhooks/register", payload)
        
        logger.info(f"Webhook registered: {response.get('webhook_id', 'unknown')}")
        return response
    
    async def send_notification(
        self,
        channel: str,
        message: str,
        recipients: List[str]
    ) -> Dict[str, Any]:
        """
        Send a notification through watsonx Orchestrate.
        
        Args:
            channel: Notification channel (email, slack, etc.)
            message: Notification message
            recipients: List of recipients
            
        Returns:
            Notification result
        """
        logger.info(f"Sending notification via {channel} to {len(recipients)} recipients")
        
        payload = {
            "channel": channel,
            "message": message,
            "recipients": recipients,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = await self._make_request("POST", "notifications/send", payload)
        
        logger.info(f"Notification sent: {response.get('status', 'unknown')}")
        return response
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the Orchestrate API connection.
        
        Returns:
            Health status
        """
        if self.mock_mode:
            return {
                "status": "healthy",
                "mock_mode": True,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            response = await self._make_request("GET", "health")
            return {
                "status": "healthy",
                "mock_mode": False,
                "api_response": response,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "mock_mode": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Made with Bob
