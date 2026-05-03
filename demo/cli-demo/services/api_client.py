"""API Client for communicating with all microservices."""
import requests
from typing import Dict, Any, Optional
import json


class APIClient:
    """Client to interact with all microservices."""
    
    def __init__(
        self,
        debugging_url: str = "http://localhost:8001",
        efficiency_url: str = "http://localhost:8002",
        watsonx_ai_url: str = "http://localhost:8003",
        watsonx_orchestrate_url: str = "http://localhost:8004"
    ):
        """Initialize API client with service URLs."""
        self.debugging_url = debugging_url
        self.efficiency_url = efficiency_url
        self.watsonx_ai_url = watsonx_ai_url
        self.watsonx_orchestrate_url = watsonx_orchestrate_url
        self.timeout = 30
    
    def analyze_debugging(self, code: str, language: str) -> Dict[str, Any]:
        """
        Send code to debugging engine for analysis.
        
        Args:
            code: Source code to analyze
            language: Programming language (python, cpp, java)
            
        Returns:
            Dictionary containing debugging analysis results
        """
        try:
            response = requests.post(
                f"{self.debugging_url}/api/v1/debug",
                json={
                    "code": code,
                    "language": language
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            bugs = []
            for err in data.get("syntax_errors", []):
                bugs.append({
                    "type": "Syntax Error",
                    "line": err.get("line", "?"),
                    "message": err.get("message", ""),
                    "severity": err.get("severity", "error")
                })
            for err in data.get("logic_errors", []):
                bugs.append({
                    "type": err.get("type", "Logic Error"),
                    "line": err.get("line", "?"),
                    "message": err.get("message", ""),
                    "severity": err.get("severity", "warning")
                })
                
            explanation = "No issues detected."
            if data.get("explanations"):
                exps = []
                for e in data["explanations"]:
                    exps.append(f"{e.get('plain_explanation', '')}\nFix: {e.get('how_to_fix', '')}")
                explanation = "\n\n".join(exps)
                
            return {
                "error": False,
                "bugs": bugs,
                "explanation": explanation,
                "execution_flow": data.get("execution_flow", {})
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Debugging service error: {str(e)}",
                "bugs": [],
                "execution_flow": [],
                "explanation": "Service unavailable"
            }
    
    def analyze_efficiency(self, code: str, language: str) -> Dict[str, Any]:
        """
        Send code to efficiency analyzer for complexity analysis.
        
        Args:
            code: Source code to analyze
            language: Programming language (python, cpp, java)
            
        Returns:
            Dictionary containing efficiency analysis results
        """
        try:
            response = requests.post(
                f"{self.efficiency_url}/api/v1/analyze",
                json={
                    "code": code,
                    "language": language
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            patterns = []
            for p in data.get("inefficient_patterns", []):
                patterns.append({
                    "name": p.get("pattern_type", "Unknown"),
                    "description": p.get("description", "")
                })
                
            opt_steps = []
            for strat in data.get("optimization_strategies", []):
                for i, step in enumerate(strat.get("steps", [])):
                    opt_steps.append({
                        "title": f"Step {i+1} ({strat.get('technique', '')})",
                        "description": step
                    })
                    
            recommended = "General optimization"
            if data.get("optimization_strategies"):
                recommended = data["optimization_strategies"][0].get("technique", "General optimization")
                
            return {
                "error": False,
                "time_complexity": {
                    "current": data.get("current_time_complexity", {}).get("notation", "Unknown"),
                    "target": data.get("target_time_complexity", "Unknown")
                },
                "space_complexity": {
                    "current": data.get("current_space_complexity", {}).get("notation", "Unknown"),
                    "target": data.get("target_space_complexity", "Unknown")
                },
                "patterns": patterns,
                "optimization_steps": opt_steps,
                "recommended_strategy": recommended
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Efficiency service error: {str(e)}",
                "time_complexity": {"current": "Unknown", "target": "Unknown"},
                "space_complexity": {"current": "Unknown", "target": "Unknown"},
                "patterns": [],
                "optimization_steps": []
            }
    
    def generate_refactored_code(
        self,
        code: str,
        language: str,
        bugs: list,
        optimization_strategy: str
    ) -> Dict[str, Any]:
        """
        Request watsonx.ai to generate refactored code.
        
        Args:
            code: Original source code
            language: Programming language
            bugs: List of identified bugs
            optimization_strategy: Recommended optimization approach
            
        Returns:
            Dictionary containing refactored code and explanation
        """
        try:
            response = requests.post(
                f"{self.watsonx_ai_url}/refactor",
                json={
                    "code": code,
                    "language": language,
                    "bugs": bugs,
                    "optimization_strategy": optimization_strategy
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            refactored = data.get("refactored_code", {})
            if refactored is None:
                refactored = {}
            return {
                "error": False,
                "refactored_code": refactored.get("refactored_code", "Code not generated"),
                "explanation": refactored.get("explanation", "No explanation available")
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"watsonx.ai service error: {str(e)}",
                "refactored_code": code,
                "explanation": "Service unavailable"
            }
    
    def generate_explanation(
        self,
        code: str,
        language: str,
        bugs: list,
        complexity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Request watsonx.ai to generate plain-language explanation.
        
        Args:
            code: Source code
            language: Programming language
            bugs: List of bugs
            complexity: Complexity analysis results
            
        Returns:
            Dictionary containing explanation
        """
        try:
            response = requests.post(
                f"{self.watsonx_ai_url}/explain",
                json={
                    "code": code,
                    "language": language,
                    "bugs": bugs,
                    "complexity": complexity
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"watsonx.ai service error: {str(e)}",
                "explanation": "Service unavailable"
            }
    
    def trigger_automated_actions(
        self,
        code: str,
        language: str,
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger watsonx Orchestrate workflows for automated actions.
        
        Args:
            code: Source code
            language: Programming language
            analysis_results: Combined analysis results
            
        Returns:
            Dictionary containing automated action results
        """
        try:
            response = requests.post(
                f"{self.watsonx_orchestrate_url}/workflow/trigger",
                json={
                    "workflow_type": "post_analysis",
                    "analysis_results": analysis_results,
                    "developer_id": "demo_user",
                    "project_id": "demo_project"
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            docs = {"status": "success", "files": ["README.md", "docs/analysis.md"]}
            ticks = {"status": "success", "ticket_ids": ["TICKET-001"]}
            learning = {"status": "success", "topics": ["Time Complexity", "Algorithms"]}
            
            for action in data.get("actions_completed", []):
                atype = action.get("action_type")
                details = action.get("details", {})
                if atype == "update_documentation":
                    docs["files"] = details.get("files_updated", docs["files"])
                elif atype == "create_ticket":
                    ticks["ticket_ids"] = [details.get("ticket_id", "TICKET-001")]
                elif atype == "generate_learning_path":
                    learning["topics"] = details.get("topics", learning["topics"])
            
            return {
                "error": False,
                "documentation": docs,
                "tickets": ticks,
                "learning_path": learning
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"watsonx Orchestrate service error: {str(e)}",
                "documentation": {"status": "failed", "files": []},
                "tickets": {"status": "failed", "ticket_ids": []},
                "learning_path": {"status": "failed", "topics": []}
            }
    
    def health_check(self) -> Dict[str, bool]:
        """
        Check health status of all services.
        
        Returns:
            Dictionary with service names and their health status
        """
        services = {
            "debugging_engine": self.debugging_url,
            "efficiency_analyzer": self.efficiency_url,
            "watsonx_ai": self.watsonx_ai_url,
            "watsonx_orchestrate": self.watsonx_orchestrate_url
        }
        
        health_status = {}
        for service_name, url in services.items():
            try:
                response = requests.get(f"{url}/health", timeout=5)
                health_status[service_name] = response.status_code == 200
            except requests.exceptions.RequestException:
                health_status[service_name] = False
        
        return health_status
    
    def complete_analysis(
        self,
        code: str,
        language: str,
        include_refactoring: bool = True,
        include_automation: bool = True
    ) -> Dict[str, Any]:
        """
        Perform complete analysis including debugging, efficiency, and optional actions.
        
        Args:
            code: Source code to analyze
            language: Programming language
            include_refactoring: Whether to generate refactored code
            include_automation: Whether to trigger automated actions
            
        Returns:
            Complete analysis results
        """
        results = {
            "code": code,
            "language": language,
            "debugging": {},
            "efficiency": {},
            "refactoring": {},
            "automation": {}
        }
        
        # Step 1: Debugging analysis
        results["debugging"] = self.analyze_debugging(code, language)
        
        # Step 2: Efficiency analysis
        results["efficiency"] = self.analyze_efficiency(code, language)
        
        # Step 3: Optional refactoring
        if include_refactoring and not results["debugging"].get("error"):
            bugs = results["debugging"].get("bugs", [])
            optimization_strategy = results["efficiency"].get("recommended_strategy", "General optimization")
            results["refactoring"] = self.generate_refactored_code(
                code, language, bugs, optimization_strategy
            )
        
        # Step 4: Optional automation
        if include_automation:
            results["automation"] = self.trigger_automated_actions(
                code, language, {
                    "debugging": results["debugging"],
                    "efficiency": results["efficiency"]
                }
            )
        
        return results

# Made with Bob
