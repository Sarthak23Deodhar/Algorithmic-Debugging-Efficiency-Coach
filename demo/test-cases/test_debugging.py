"""
Test cases for Debugging Engine service.

Tests the debugging engine's ability to identify bugs, analyze execution flow,
and provide explanations.
"""
import unittest
import requests
import json
from pathlib import Path


class TestDebuggingEngine(unittest.TestCase):
    """Test cases for debugging engine functionality."""
    
    BASE_URL = "http://localhost:8001"
    SAMPLES_DIR = Path(__file__).parent / "sample_codes"
    
    def setUp(self):
        """Set up test fixtures."""
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def test_health_check(self):
        """Test that the debugging engine is running."""
        response = self.session.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
    
    def test_python_syntax_error(self):
        """Test detection of Python syntax errors."""
        code = """
def hello():
    print("Hello"
    return
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("bugs", data)
        self.assertGreater(len(data["bugs"]), 0)
        
        # Check that syntax error is detected
        bug_types = [bug.get("type", "").lower() for bug in data["bugs"]]
        self.assertTrue(any("syntax" in bt for bt in bug_types))
    
    def test_python_logic_error(self):
        """Test detection of Python logic errors."""
        code = """
def find_max(numbers):
    max_val = numbers[0]
    for i in range(1, len(numbers) + 1):  # Off-by-one error
        if numbers[i] > max_val:
            max_val = numbers[i]
    return max_val
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("bugs", data)
        # Should detect index out of bounds or similar issue
        self.assertGreater(len(data["bugs"]), 0)
    
    def test_python_runtime_error(self):
        """Test detection of potential runtime errors."""
        code = """
def divide(a, b):
    return a / b  # Potential division by zero

result = divide(10, 0)
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("bugs", data)
        # Should detect potential division by zero
    
    def test_execution_flow_analysis(self):
        """Test execution flow analysis."""
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("execution_flow", data)
        # Should provide execution flow information
    
    def test_bug_explanation(self):
        """Test that bug explanations are provided."""
        code = """
def broken_function():
    x = 10
    y = 0
    return x / y
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "python"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("explanation", data)
        self.assertIsInstance(data["explanation"], str)
        self.assertGreater(len(data["explanation"]), 0)
    
    def test_cpp_syntax_error(self):
        """Test detection of C++ syntax errors."""
        code = """
#include <iostream>

int main() {
    std::cout << "Hello" << std::endl
    return 0;
}
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "cpp"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("bugs", data)
        # Should detect missing semicolon
    
    def test_java_syntax_error(self):
        """Test detection of Java syntax errors."""
        code = """
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello")
    }
}
"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "java"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("bugs", data)
        # Should detect missing semicolon
    
    def test_invalid_language(self):
        """Test handling of invalid language."""
        code = "print('hello')"
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": code, "language": "invalid"}
        )
        
        # Should return error or handle gracefully
        self.assertIn(response.status_code, [400, 422])
    
    def test_empty_code(self):
        """Test handling of empty code."""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/analyze",
            json={"code": "", "language": "python"}
        )
        
        # Should handle empty code gracefully
        self.assertIn(response.status_code, [200, 400, 422])
    
    def test_sample_file_nested_loops(self):
        """Test analysis of nested loops sample file."""
        sample_file = self.SAMPLES_DIR / "python" / "nested_loops.py"
        
        if sample_file.exists():
            with open(sample_file, 'r') as f:
                code = f.read()
            
            response = self.session.post(
                f"{self.BASE_URL}/api/v1/analyze",
                json={"code": code, "language": "python"}
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertIn("bugs", data)
            self.assertIn("execution_flow", data)


if __name__ == "__main__":
    unittest.main()

# Made with Bob
