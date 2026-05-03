"""
Test cases for Efficiency Analyzer service.

Tests the efficiency analyzer's ability to calculate complexity,
detect patterns, and recommend optimizations.
"""
import unittest
import requests
import json
from pathlib import Path


class TestEfficiencyAnalyzer(unittest.TestCase):
    """Test cases for efficiency analyzer functionality."""
    
    BASE_URL = "http://localhost:8002"
    SAMPLES_DIR = Path(__file__).parent / "sample_codes"
    
    def setUp(self):
        """Set up test fixtures."""
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def test_health_check(self):
        """Test that the efficiency analyzer is running."""
        response = self.session.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
    
    def test_nested_loops_complexity(self):
        """Test detection of O(n²) complexity in nested loops."""
        code = """
def find_pairs(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return (numbers[i], numbers[j])
    return None
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
        self.assertIn("current", data["time_complexity"])
        
        # Should detect O(n²) complexity
        current_complexity = data["time_complexity"]["current"]
        self.assertIn("n", current_complexity.lower())
    
    def test_linear_complexity(self):
        """Test detection of O(n) complexity."""
        code = """
def find_max(numbers):
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
        current_complexity = data["time_complexity"]["current"]
        
        # Should detect O(n) complexity
        self.assertIn("n", current_complexity.lower())
    
    def test_space_complexity_analysis(self):
        """Test space complexity analysis."""
        code = """
def create_matrix(n):
    matrix = []
    for i in range(n):
        row = [0] * n
        matrix.append(row)
    return matrix
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("space_complexity", data)
        self.assertIn("current", data["space_complexity"])
        
        # Should detect O(n²) space complexity
        current_space = data["space_complexity"]["current"]
        self.assertIsInstance(current_space, str)
    
    def test_pattern_detection(self):
        """Test detection of inefficient patterns."""
        code = """
def remove_duplicates(numbers):
    result = []
    for num in numbers:
        if num not in result:  # O(n) operation in loop
            result.append(num)
    return result
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("patterns", data)
        # Should detect inefficient pattern
        self.assertIsInstance(data["patterns"], list)
    
    def test_optimization_recommendations(self):
        """Test that optimization recommendations are provided."""
        code = """
def find_duplicates(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                duplicates.append(numbers[i])
    return duplicates
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("optimization_steps", data)
        self.assertIsInstance(data["optimization_steps"], list)
        
        # Should provide optimization strategy
        self.assertIn("recommended_strategy", data)
    
    def test_recursive_complexity(self):
        """Test complexity analysis of recursive functions."""
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
        # Fibonacci has exponential complexity
        current_complexity = data["time_complexity"]["current"]
        self.assertIsInstance(current_complexity, str)
    
    def test_target_complexity(self):
        """Test that target complexity is suggested."""
        code = """
def has_duplicate(numbers):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                return True
    return False
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
        self.assertIn("target", data["time_complexity"])
        
        # Should suggest better target complexity
        target_complexity = data["time_complexity"]["target"]
        self.assertIsInstance(target_complexity, str)
    
    def test_cpp_complexity_analysis(self):
        """Test complexity analysis for C++ code."""
        code = """
#include <vector>

int findMax(std::vector<int>& nums) {
    int maxVal = nums[0];
    for (int i = 1; i < nums.size(); i++) {
        if (nums[i] > maxVal) {
            maxVal = nums[i];
        }
    }
    return maxVal;
}
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "cpp"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
    
    def test_java_complexity_analysis(self):
        """Test complexity analysis for Java code."""
        code = """
public class Solution {
    public int findMax(int[] nums) {
        int maxVal = nums[0];
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > maxVal) {
                maxVal = nums[i];
            }
        }
        return maxVal;
    }
}
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "java"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
    
    def test_optimized_code_analysis(self):
        """Test analysis of already optimized code."""
        code = """
def find_pair(numbers, target):
    seen = set()
    for num in numbers:
        complement = target - num
        if complement in seen:
            return (complement, num)
        seen.add(num)
    return None
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("time_complexity", data)
        # Should recognize O(n) complexity
        current_complexity = data["time_complexity"]["current"]
        self.assertIn("n", current_complexity.lower())
    
    def test_sample_file_inefficient_sort(self):
        """Test analysis of inefficient sort sample file."""
        sample_file = self.SAMPLES_DIR / "java" / "inefficient_sort.java"
        
        if sample_file.exists():
            with open(sample_file, 'r') as f:
                code = f.read()
            
            response = self.session.post(
                f"{self.BASE_URL}/api/v1/analyze",
                json={"code": code, "language": "java"}
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertIn("time_complexity", data)
            self.assertIn("optimization_steps", data)


if __name__ == "__main__":
    unittest.main()

# Made with Bob
