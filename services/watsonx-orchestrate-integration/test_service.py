"""Test script for watsonx Orchestrate Integration Service"""

import asyncio
import requests
from app.models.request import WorkflowRequest, WorkflowType, SkillGap

BASE_URL = "http://localhost:8004"


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def test_post_analysis_workflow():
    """Test post-analysis workflow"""
    print("\n=== Testing Post-Analysis Workflow ===")
    
    workflow_request = {
        "workflow_type": "post_analysis",
        "analysis_results": {
            "file_path": "src/algorithms/sort.py",
            "complexity": {
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)"
            },
            "issues": [
                "Inefficient nested loops",
                "Missing edge case handling",
                "Poor variable naming"
            ],
            "suggestions": [
                "Replace bubble sort with merge sort",
                "Add input validation",
                "Use descriptive variable names"
            ]
        },
        "developer_id": "dev123",
        "project_id": "proj456"
    }
    
    response = requests.post(f"{BASE_URL}/workflow/trigger", json=workflow_request)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Job ID: {result['job_id']}")
    print(f"Status: {result['status']}")
    
    # Check status
    job_id = result['job_id']
    asyncio.sleep(2)  # Wait for workflow to complete
    
    status_response = requests.get(f"{BASE_URL}/workflow/status/{job_id}")
    print(f"\nWorkflow Status: {status_response.json()}")


def test_optimization_workflow():
    """Test optimization workflow"""
    print("\n=== Testing Optimization Workflow ===")
    
    workflow_request = {
        "workflow_type": "optimization",
        "analysis_results": {
            "file_path": "src/algorithms/sort.py",
            "before_complexity": {
                "time": "O(n^2)",
                "space": "O(1)"
            },
            "after_complexity": {
                "time": "O(n log n)",
                "space": "O(n)"
            },
            "changes_made": [
                "Replaced bubble sort with merge sort",
                "Improved time complexity by 75%"
            ],
            "performance_improvement": {
                "percentage": 75,
                "execution_time_ms": "reduced from 1000ms to 250ms"
            },
            "related_ticket_ids": ["PROJ-1001"]
        },
        "developer_id": "dev123",
        "project_id": "proj456"
    }
    
    response = requests.post(f"{BASE_URL}/workflow/trigger", json=workflow_request)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def test_developer_growth_workflow():
    """Test developer growth workflow"""
    print("\n=== Testing Developer Growth Workflow ===")
    
    workflow_request = {
        "workflow_type": "developer_growth",
        "analysis_results": {
            "submissions": [
                {
                    "file": "solution1.py",
                    "issues": ["inefficient dynamic programming", "missing memoization"]
                },
                {
                    "file": "solution2.py",
                    "issues": ["poor graph traversal", "inefficient BFS implementation"]
                },
                {
                    "file": "solution3.py",
                    "issues": ["dynamic programming optimization needed"]
                }
            ],
            "skill_level": "intermediate"
        },
        "developer_id": "dev123",
        "project_id": "proj456"
    }
    
    response = requests.post(f"{BASE_URL}/workflow/trigger", json=workflow_request)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    print("=" * 60)
    print("watsonx Orchestrate Integration Service - Test Suite")
    print("=" * 60)
    
    try:
        test_health()
        test_post_analysis_workflow()
        test_optimization_workflow()
        test_developer_growth_workflow()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to service.")
        print("Make sure the service is running: python -m app.handler")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")

# Made with Bob
