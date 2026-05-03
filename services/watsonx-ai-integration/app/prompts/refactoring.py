"""
Prompt templates for AI-powered code refactoring
"""

from typing import Optional, List


def build_refactoring_prompt(
    original_code: str,
    language: str,
    inefficient_patterns: List[str],
    target_complexity: Optional[str] = None,
    optimization_focus: str = "balanced"
) -> str:
    """
    Build a structured prompt for code refactoring
    
    Args:
        original_code: Code to be refactored
        language: Programming language
        inefficient_patterns: List of detected inefficient patterns
        target_complexity: Target complexity (e.g., "O(n log n)")
        optimization_focus: Primary optimization focus
        
    Returns:
        Formatted prompt string for watsonx.ai
    """
    
    prompt = f"""You are an expert code optimizer specializing in algorithmic efficiency and performance optimization.

TASK: Refactor and optimize the following {language} code while preserving its functionality.

ORIGINAL CODE:
```{language}
{original_code}
```
"""
    
    # Add detected inefficiencies
    if inefficient_patterns:
        prompt += "\nDETECTED INEFFICIENCIES:\n"
        for pattern in inefficient_patterns:
            pattern_descriptions = {
                "nested_loops": "Nested loops causing O(n²) or worse time complexity",
                "redundant_computation": "Repeated calculations that could be cached",
                "inefficient_data_structure": "Using suboptimal data structures for the operations",
                "unnecessary_iterations": "Multiple passes over data when one would suffice",
                "O(n^2)_time": "Quadratic time complexity that can be improved",
                "excessive_memory": "Using more memory than necessary",
                "unoptimized_search": "Linear search where hash-based lookup would be better"
            }
            description = pattern_descriptions.get(pattern, pattern)
            prompt += f"- {description}\n"
    
    # Add target complexity if specified
    if target_complexity:
        prompt += f"""
TARGET COMPLEXITY:
{target_complexity}
"""
    
    # Add optimization focus
    focus_guidance = {
        "time_complexity": "Focus on reducing time complexity. Use optimal algorithms and data structures.",
        "space_complexity": "Focus on reducing space complexity. Minimize memory usage.",
        "readability": "Focus on improving code clarity while maintaining efficiency.",
        "balanced": "Balance time efficiency, space efficiency, and code readability."
    }
    
    prompt += f"""
OPTIMIZATION FOCUS:
{focus_guidance.get(optimization_focus, focus_guidance["balanced"])}

REFACTORING REQUIREMENTS:
1. Preserve the original functionality exactly
2. Apply appropriate algorithmic optimizations (e.g., use hash maps instead of nested loops)
3. Improve time and/or space complexity
4. Maintain or improve code readability
5. Add comments explaining the optimizations
6. Handle all edge cases from the original code

OUTPUT FORMAT (JSON):
{{
    "refactored_code": "your optimized {language} code here",
    "changes_made": ["list of specific changes applied"],
    "complexity_before": {{
        "time": "original time complexity",
        "space": "original space complexity"
    }},
    "complexity_after": {{
        "time": "new time complexity",
        "space": "new space complexity"
    }},
    "explanation": "detailed explanation of each optimization and why it improves performance",
    "trade_offs": "any trade-offs made (e.g., increased space for better time)"
}}

Refactor the code now:"""
    
    return prompt


def build_refactoring_prompt_with_examples() -> str:
    """
    Build a few-shot refactoring prompt with examples
    
    Returns:
        Prompt with example refactoring cases
    """
    
    prompt = """You are an expert code optimizer. Here are examples of code refactoring:

EXAMPLE 1 - Nested Loops to Hash Map:

Original Code (Python):
```python
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates
```

Refactored Code:
```json
{
    "refactored_code": "def find_duplicates(arr):\\n    seen = set()\\n    duplicates = set()\\n    for num in arr:\\n        if num in seen:\\n            duplicates.add(num)\\n        seen.add(num)\\n    return list(duplicates)",
    "changes_made": [
        "Replaced nested loops with single pass using hash set",
        "Used set for O(1) membership testing",
        "Eliminated redundant 'not in duplicates' check"
    ],
    "complexity_before": {
        "time": "O(n²)",
        "space": "O(k) where k is number of duplicates"
    },
    "complexity_after": {
        "time": "O(n)",
        "space": "O(n)"
    },
    "explanation": "The original code used nested loops to compare every pair of elements (O(n²)). The refactored version uses a hash set to track seen elements, allowing O(1) lookups. This reduces time complexity from O(n²) to O(n) at the cost of O(n) space.",
    "trade_offs": "Increased space complexity from O(k) to O(n), but dramatically improved time complexity"
}
```

EXAMPLE 2 - Redundant Computation to Memoization:

Original Code (Python):
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

Refactored Code:
```json
{
    "refactored_code": "def fibonacci(n, memo=None):\\n    if memo is None:\\n        memo = {}\\n    if n in memo:\\n        return memo[n]\\n    if n <= 1:\\n        return n\\n    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)\\n    return memo[n]",
    "changes_made": [
        "Added memoization to cache computed values",
        "Eliminated redundant recursive calls"
    ],
    "complexity_before": {
        "time": "O(2ⁿ)",
        "space": "O(n) call stack"
    },
    "complexity_after": {
        "time": "O(n)",
        "space": "O(n)"
    },
    "explanation": "The original recursive solution recomputes the same Fibonacci numbers many times. By adding memoization, each number is computed only once and cached. This reduces exponential time complexity to linear.",
    "trade_offs": "Added O(n) space for memoization, but reduced time from exponential to linear"
}
```

Now refactor the following code:
"""
    
    return prompt

# Made with Bob