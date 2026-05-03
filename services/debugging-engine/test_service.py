"""
Simple test script to verify the Debugging Engine service
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.models.request import CodeSubmission, ProgrammingLanguage
from app.parsers.python_parser import PythonParser
from app.services.execution_flow import ExecutionFlowAnalyzer
from app.services.root_cause import RootCauseIdentifier
from app.services.explainer import BugExplainer


def test_python_parser():
    """Test Python parser"""
    print("\n=== Testing Python Parser ===")
    parser = PythonParser()
    
    code = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""
    
    result = parser.parse(code)
    print(f"✓ Parse successful: {result['success']}")
    print(f"✓ Functions found: {len(result['functions'])}")
    print(f"✓ Control structures: {len(result['control_structures'])}")
    return result['success']


def test_execution_flow():
    """Test execution flow analyzer"""
    print("\n=== Testing Execution Flow Analyzer ===")
    analyzer = ExecutionFlowAnalyzer()
    
    code = """
def add(a, b):
    return a + b

result = add(5, 3)
"""
    
    flow = analyzer.analyze(code, ProgrammingLanguage.PYTHON)
    print(f"✓ Entry point: {flow['entry_point']}")
    print(f"✓ Functions: {len(flow['functions'])}")
    return True


def test_root_cause_identifier():
    """Test root cause identifier"""
    print("\n=== Testing Root Cause Identifier ===")
    identifier = RootCauseIdentifier()
    
    # Code with syntax error
    code = """
def broken():
    return "missing quote
"""
    
    parser = PythonParser()
    parsed = parser.parse(code)
    
    result = identifier.identify(code, ProgrammingLanguage.PYTHON, parsed)
    print(f"✓ Syntax errors found: {len(result['syntax_errors'])}")
    print(f"✓ Logic errors found: {len(result['logic_errors'])}")
    print(f"✓ Root causes identified: {len(result['root_causes'])}")
    return True


def test_bug_explainer():
    """Test bug explainer"""
    print("\n=== Testing Bug Explainer ===")
    explainer = BugExplainer()
    
    syntax_errors = [{
        'line': 2,
        'message': 'invalid syntax',
        'code_snippet': 'return "missing quote'
    }]
    
    explanations = explainer.explain(syntax_errors, [], [])
    print(f"✓ Explanations generated: {len(explanations)}")
    if explanations:
        print(f"✓ First explanation type: {explanations[0]['error_type']}")
    return len(explanations) > 0


def test_request_model():
    """Test request model validation"""
    print("\n=== Testing Request Model ===")
    
    try:
        submission = CodeSubmission(
            language=ProgrammingLanguage.PYTHON,
            code="print('Hello, World!')",
            context="Test code"
        )
        print(f"✓ Valid submission created: {submission.language}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Debugging Engine Service - Component Tests")
    print("=" * 60)
    
    tests = [
        ("Python Parser", test_python_parser),
        ("Execution Flow Analyzer", test_execution_flow),
        ("Root Cause Identifier", test_root_cause_identifier),
        ("Bug Explainer", test_bug_explainer),
        ("Request Model", test_request_model),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Made with Bob
