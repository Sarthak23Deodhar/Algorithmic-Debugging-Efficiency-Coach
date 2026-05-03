"""
Test script for Efficiency Analyzer service
"""

import requests
import json

BASE_URL = "http://localhost:8002"


def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_nested_loops():
    """Test analysis of nested loops"""
    print("Testing nested loops analysis...")
    
    code = """def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates"""
    
    request_data = {
        "language": "python",
        "code": code,
        "context": "Array size can be up to 10000 elements"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=request_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Time Complexity: {result['current_time_complexity']['notation']}")
        print(f"Space Complexity: {result['current_space_complexity']['notation']}")
        print(f"Target Time: {result['target_time_complexity']}")
        print(f"Patterns Found: {len(result['inefficient_patterns'])}")
        print(f"Strategies: {len(result['optimization_strategies'])}")
        print(f"Overall Score: {result['overall_score']}")
        
        if result['inefficient_patterns']:
            print("\nInefficient Patterns:")
            for pattern in result['inefficient_patterns']:
                print(f"  - {pattern['pattern_type']}: {pattern['description']}")
        
        if result['optimization_strategies']:
            print("\nOptimization Strategies:")
            for strategy in result['optimization_strategies']:
                print(f"  - {strategy['technique']}: {strategy['complexity_improvement']}")
        
        if result['estimated_improvement']:
            print("\nEstimated Improvements:")
            for size, improvement in result['estimated_improvement'].items():
                print(f"  - {size}: {improvement}")
    else:
        print(f"Error: {response.text}")
    print()


def test_recursion():
    """Test analysis of recursive function"""
    print("Testing recursion analysis...")
    
    code = """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""
    
    request_data = {
        "language": "python",
        "code": code
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=request_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Time Complexity: {result['current_time_complexity']['notation']}")
        print(f"Target Time: {result['target_time_complexity']}")
        print(f"Patterns Found: {len(result['inefficient_patterns'])}")
        print(f"Overall Score: {result['overall_score']}")
        
        if result['inefficient_patterns']:
            print("\nInefficient Patterns:")
            for pattern in result['inefficient_patterns']:
                print(f"  - {pattern['pattern_type']}: {pattern['description']}")
    else:
        print(f"Error: {response.text}")
    print()


def test_efficient_code():
    """Test analysis of efficient code"""
    print("Testing efficient code analysis...")
    
    code = """def find_duplicates(arr):
    seen = set()
    duplicates = set()
    for num in arr:
        if num in seen:
            duplicates.add(num)
        seen.add(num)
    return list(duplicates)"""
    
    request_data = {
        "language": "python",
        "code": code
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=request_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Time Complexity: {result['current_time_complexity']['notation']}")
        print(f"Space Complexity: {result['current_space_complexity']['notation']}")
        print(f"Patterns Found: {len(result['inefficient_patterns'])}")
        print(f"Overall Score: {result['overall_score']}")
    else:
        print(f"Error: {response.text}")
    print()


def test_string_concatenation():
    """Test detection of string concatenation in loop"""
    print("Testing string concatenation pattern...")
    
    code = """def build_string(items):
    result = ""
    for item in items:
        result += str(item)
    return result"""
    
    request_data = {
        "language": "python",
        "code": code
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=request_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Time Complexity: {result['current_time_complexity']['notation']}")
        print(f"Patterns Found: {len(result['inefficient_patterns'])}")
        
        if result['inefficient_patterns']:
            print("\nInefficient Patterns:")
            for pattern in result['inefficient_patterns']:
                print(f"  - {pattern['pattern_type']}: {pattern['description']}")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Efficiency Analyzer Service Tests")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_nested_loops()
        test_recursion()
        test_efficient_code()
        test_string_concatenation()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to service.")
        print("Make sure the service is running on http://localhost:8002")
    except Exception as e:
        print(f"Error: {e}")

# Made with Bob
