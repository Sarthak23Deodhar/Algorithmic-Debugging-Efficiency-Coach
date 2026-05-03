"""
Test script for watsonx.ai Integration service
"""

import asyncio
import json
from app.models.request import (
    CodeGenerationRequest,
    RefactoringRequest,
    ExplanationRequest,
    ProgrammingLanguage,
    OptimizationTarget
)
from app.services.watsonx_client import WatsonxClient
from app.services.code_generator import CodeGeneratorService
from app.services.refactoring import RefactoringService
from app.services.explainer import ExplainerService


async def test_code_generation():
    """Test code generation service"""
    print("\n" + "="*60)
    print("Testing Code Generation Service")
    print("="*60)
    
    client = WatsonxClient(mock_mode=True)
    generator = CodeGeneratorService(client)
    
    request = CodeGenerationRequest(
        problem_description="Find all pairs in an array that sum to a target value",
        language=ProgrammingLanguage.PYTHON,
        constraints="Must be O(n) time complexity",
        optimization_target=OptimizationTarget.TIME_COMPLEXITY,
        include_comments=True,
        examples=[
            {"input": "[2, 7, 11, 15], target=9", "output": "[(0, 1)]"}
        ]
    )
    
    result = await generator.generate_code(request)
    
    print(f"\n✓ Success: {result['success']}")
    print(f"✓ Processing time: {result['processing_time_ms']:.2f}ms")
    print(f"✓ Model used: {result['model_used']}")
    print(f"✓ Confidence: {result['confidence_score']:.2f}")
    
    if result['success']:
        code = result['generated_code']
        print(f"\n✓ Generated Code:")
        print(f"  Language: {code.language}")
        print(f"  Algorithm: {code.algorithm_used}")
        print(f"  Time Complexity: {code.complexity_analysis.get('time')}")
        print(f"  Space Complexity: {code.complexity_analysis.get('space')}")
        print(f"\n  Code:\n{code.code}")


async def test_code_refactoring():
    """Test code refactoring service"""
    print("\n" + "="*60)
    print("Testing Code Refactoring Service")
    print("="*60)
    
    client = WatsonxClient(mock_mode=True)
    refactoring = RefactoringService(client)
    
    original_code = """def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates"""
    
    request = RefactoringRequest(
        original_code=original_code,
        language=ProgrammingLanguage.PYTHON,
        inefficient_patterns=["nested_loops", "O(n^2)_time"],
        target_complexity="O(n) time",
        optimization_focus=OptimizationTarget.TIME_COMPLEXITY,
        include_explanation=True
    )
    
    result = await refactoring.refactor_code(request)
    
    print(f"\n✓ Success: {result['success']}")
    print(f"✓ Processing time: {result['processing_time_ms']:.2f}ms")
    print(f"✓ Confidence: {result['confidence_score']:.2f}")
    
    if result['success']:
        refactored = result['refactored_code']
        print(f"\n✓ Changes Made:")
        for change in refactored.changes_made:
            print(f"  - {change}")
        
        print(f"\n✓ Complexity Improvement:")
        print(f"  Before: {refactored.complexity_improvement['before']}")
        print(f"  After: {refactored.complexity_improvement['after']}")
        
        print(f"\n✓ Refactored Code:\n{refactored.refactored_code}")


async def test_code_explanation():
    """Test code explanation service"""
    print("\n" + "="*60)
    print("Testing Code Explanation Service")
    print("="*60)
    
    client = WatsonxClient(mock_mode=True)
    explainer = ExplainerService(client)
    
    code = """def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)"""
    
    request = ExplanationRequest(
        code=code,
        language=ProgrammingLanguage.PYTHON,
        explanation_level="beginner",
        focus_areas=["algorithm", "recursion"],
        include_analogies=True
    )
    
    result = await explainer.explain_code(request)
    
    print(f"\n✓ Success: {result['success']}")
    print(f"✓ Processing time: {result['processing_time_ms']:.2f}ms")
    print(f"✓ Confidence: {result['confidence_score']:.2f}")
    
    if result['success']:
        explanation = result['explanation']
        print(f"\n✓ Summary:\n  {explanation.summary}")
        
        print(f"\n✓ Key Concepts:")
        for concept in explanation.key_concepts:
            print(f"  - {concept}")
        
        print(f"\n✓ Potential Issues:")
        for issue in explanation.potential_issues:
            print(f"  - {issue.get('type')}: {issue.get('description')}")
        
        print(f"\n✓ Suggestions:")
        for suggestion in explanation.suggestions:
            print(f"  - {suggestion}")
        
        if explanation.analogies:
            print(f"\n✓ Analogies:")
            for analogy in explanation.analogies:
                print(f"  - {analogy}")


async def test_watsonx_client():
    """Test watsonx client"""
    print("\n" + "="*60)
    print("Testing watsonx.ai Client")
    print("="*60)
    
    client = WatsonxClient(mock_mode=True)
    
    print(f"\n✓ Mock mode: {client.mock_mode}")
    print(f"✓ Connected: {client.is_connected()}")
    print(f"✓ Primary model: {client.primary_model}")
    print(f"✓ Fast model: {client.fast_model}")
    
    # Test generation
    prompt = "Generate a Python function to calculate fibonacci"
    response = await client.generate(prompt, max_tokens=100)
    
    print(f"\n✓ Generation test:")
    print(f"  Model: {response['model_id']}")
    print(f"  Mock mode: {response.get('mock_mode', False)}")
    print(f"  Response length: {len(response['results'][0]['generated_text'])} chars")


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("watsonx.ai Integration Service - Test Suite")
    print("="*60)
    
    try:
        # Test individual components
        await test_watsonx_client()
        await test_code_generation()
        await test_code_refactoring()
        await test_code_explanation()
        
        print("\n" + "="*60)
        print("✓ All tests completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob