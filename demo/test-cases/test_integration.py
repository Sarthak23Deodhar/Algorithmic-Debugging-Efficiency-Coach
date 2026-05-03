"""
End-to-end integration tests for the complete system.

Tests the integration between all services including debugging engine,
efficiency analyzer, watsonx.ai, and watsonx Orchestrate.
"""
import unittest
import requests
import json
import time
from pathlib import Path


class TestSystemIntegration(unittest.TestCase):
    """End-to-end integration tests."""
    
    DEBUGGING_URL = "http://localhost:8001"
    EFFICIENCY_URL = "http://localhost:8002"
    WATSONX_AI_URL = "http://localhost:8003"
    WATSONX_ORCHESTRATE_URL = "http://localhost:8004"
    
    def setUp(self):
        """Set up test fixtures."""
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def test_all_services_health(self):
        """Test that all services are running."""
        services = {
            "Debugging Engine": self.DEBUGGING_URL,
            "Efficiency Analyzer": self.EFFICIENCY_URL,
            "watsonx.ai Integration": self.WATSONX_AI_URL,
            "watsonx Orchestrate": self.WATSONX_ORCHESTRATE_URL
        }
        
        for service_name, url in services.items():
            with self.subTest(service=service_name):
                try:
                    response = self.session.get(f"{url}/health", timeout=5)
                    self.assertEqual(
                        response.status_code, 200,
                        f"{service_name} is not responding"
                    )
                except requests.exceptions.RequestException as e:
                    self.fail(f"{service_name} is not accessible: {str(e)}")
    
    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow from debugging to automation."""
        code = """
def find_duplicates(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                duplicates.append(numbers[i])
    return duplicates
"""
        
        # Step 1: Debugging analysis
        debug_response = self.session.post(
            f"{self.DEBUGGING_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        self.assertEqual(debug_response.status_code, 200)
        debug_data = debug_response.json()
        
        # Step 2: Efficiency analysis
        efficiency_response = self.session.post(
            f"{self.EFFICIENCY_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        self.assertEqual(efficiency_response.status_code, 200)
        efficiency_data = efficiency_response.json()
        
        # Step 3: Request refactoring
        refactor_response = self.session.post(
            f"{self.WATSONX_AI_URL}/api/v1/refactor",
            json={
                "code": code,
                "language": "python",
                "bugs": debug_data.get("bugs", []),
                "optimization_strategy": efficiency_data.get("recommended_strategy", "")
            }
        )
        self.assertEqual(refactor_response.status_code, 200)
        refactor_data = refactor_response.json()
        
        # Step 4: Trigger automation
        automation_response = self.session.post(
            f"{self.WATSONX_ORCHESTRATE_URL}/api/v1/automate",
            json={
                "code": code,
                "language": "python",
                "analysis_results": {
                    "debugging": debug_data,
                    "efficiency": efficiency_data
                }
            }
        )
        self.assertEqual(automation_response.status_code, 200)
        automation_data = automation_response.json()
        
        # Verify all steps completed
        self.assertIn("bugs", debug_data)
        self.assertIn("time_complexity", efficiency_data)
        self.assertIn("refactored_code", refactor_data)
        self.assertIn("documentation", automation_data)
    
    def test_debugging_to_efficiency_pipeline(self):
        """Test pipeline from debugging to efficiency analysis."""
        code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
        
        # First get debugging results
        debug_response = self.session.post(
            f"{self.DEBUGGING_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        self.assertEqual(debug_response.status_code, 200)
        
        # Then get efficiency results
        efficiency_response = self.session.post(
            f"{self.EFFICIENCY_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        self.assertEqual(efficiency_response.status_code, 200)
        
        # Both should succeed
        debug_data = debug_response.json()
        efficiency_data = efficiency_response.json()
        
        self.assertIsInstance(debug_data, dict)
        self.assertIsInstance(efficiency_data, dict)
    
    def test_watsonx_ai_refactoring_integration(self):
        """Test watsonx.ai refactoring with analysis results."""
        code = """
def slow_search(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1
"""
        
        # Get efficiency analysis first
        efficiency_response = self.session.post(
            f"{self.EFFICIENCY_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        self.assertEqual(efficiency_response.status_code, 200)
        efficiency_data = efficiency_response.json()
        
        # Request refactoring based on analysis
        refactor_response = self.session.post(
            f"{self.WATSONX_AI_URL}/api/v1/refactor",
            json={
                "code": code,
                "language": "python",
                "bugs": [],
                "optimization_strategy": efficiency_data.get("recommended_strategy", "")
            }
        )
        self.assertEqual(refactor_response.status_code, 200)
        refactor_data = refactor_response.json()
        
        # Should provide refactored code
        self.assertIn("refactored_code", refactor_data)
        self.assertIsInstance(refactor_data["refactored_code"], str)
    
    def test_watsonx_orchestrate_automation(self):
        """Test watsonx Orchestrate automation workflows."""
        analysis_results = {
            "debugging": {
                "bugs": [
                    {"type": "logic_error", "line": 5, "message": "Potential issue"}
                ],
                "explanation": "Code has logic issues"
            },
            "efficiency": {
                "time_complexity": {"current": "O(n²)", "target": "O(n)"},
                "recommended_strategy": "Use hash map"
            }
        }
        
        automation_response = self.session.post(
            f"{self.WATSONX_ORCHESTRATE_URL}/api/v1/automate",
            json={
                "code": "def test(): pass",
                "language": "python",
                "analysis_results": analysis_results
            }
        )
        
        self.assertEqual(automation_response.status_code, 200)
        automation_data = automation_response.json()
        
        # Should provide automation results
        self.assertIn("documentation", automation_data)
        self.assertIn("tickets", automation_data)
        self.assertIn("learning_path", automation_data)
    
    def test_multi_language_support(self):
        """Test that all services support multiple languages."""
        test_codes = {
            "python": "def test(): pass",
            "cpp": "int main() { return 0; }",
            "java": "public class Test { }"
        }
        
        for language, code in test_codes.items():
            with self.subTest(language=language):
                # Test debugging engine
                debug_response = self.session.post(
                    f"{self.DEBUGGING_URL}/api/v1/analyze",
                    json={"code": code, "language": language}
                )
                self.assertEqual(debug_response.status_code, 200)
                
                # Test efficiency analyzer
                efficiency_response = self.session.post(
                    f"{self.EFFICIENCY_URL}/api/v1/analyze",
                    json={"code": code, "language": language}
                )
                self.assertEqual(efficiency_response.status_code, 200)
    
    def test_error_handling_across_services(self):
        """Test error handling when services receive invalid input."""
        invalid_code = "this is not valid code in any language"
        
        # All services should handle invalid code gracefully
        services = [
            (self.DEBUGGING_URL, "/api/v1/analyze"),
            (self.EFFICIENCY_URL, "/api/v1/analyze")
        ]
        
        for base_url, endpoint in services:
            with self.subTest(service=base_url):
                response = self.session.post(
                    f"{base_url}{endpoint}",
                    json={"code": invalid_code, "language": "python"}
                )
                
                # Should return 200 with error info or 4xx status
                self.assertIn(response.status_code, [200, 400, 422, 500])
    
    def test_concurrent_requests(self):
        """Test system handles concurrent requests."""
        import concurrent.futures
        
        code = "def test(): return 42"
        
        def make_request():
            response = self.session.post(
                f"{self.DEBUGGING_URL}/api/v1/analyze",
                json={"code": code, "language": "python"}
            )
            return response.status_code
        
        # Make 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        self.assertTrue(all(status == 200 for status in results))
    
    def test_response_time_performance(self):
        """Test that services respond within acceptable time."""
        code = """
def simple_function(x):
    return x * 2
"""
        
        services = [
            (self.DEBUGGING_URL, "/api/v1/analyze"),
            (self.EFFICIENCY_URL, "/api/v1/analyze")
        ]
        
        for base_url, endpoint in services:
            with self.subTest(service=base_url):
                start_time = time.time()
                response = self.session.post(
                    f"{base_url}{endpoint}",
                    json={"code": code, "language": "python"}
                )
                elapsed_time = time.time() - start_time
                
                self.assertEqual(response.status_code, 200)
                # Should respond within 30 seconds
                self.assertLess(elapsed_time, 30.0)


if __name__ == "__main__":
    unittest.main()

# Made with Bob
