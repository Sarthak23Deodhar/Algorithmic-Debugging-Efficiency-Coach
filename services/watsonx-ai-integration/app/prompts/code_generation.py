"""
Prompt templates for AI-powered code generation
"""

from typing import Optional, List, Dict, Any


def build_generation_prompt(
    problem_description: str,
    language: str,
    constraints: Optional[str] = None,
    optimization_target: str = "balanced",
    examples: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Build a structured prompt for code generation
    
    Args:
        problem_description: Natural language description of the problem
        language: Target programming language
        constraints: Optional constraints (time/space complexity)
        optimization_target: What to optimize for
        examples: Optional input/output examples
        
    Returns:
        Formatted prompt string for watsonx.ai
    """
    
    # Base prompt with few-shot examples
    prompt = f"""You are an expert software engineer specializing in algorithmic problem solving and code optimization.

TASK: Generate optimized {language} code to solve the following problem.

PROBLEM DESCRIPTION:
{problem_description}
"""
    
    # Add constraints if provided
    if constraints:
        prompt += f"""
CONSTRAINTS:
{constraints}
"""
    
    # Add optimization target
    optimization_guidance = {
        "time_complexity": "Prioritize time efficiency. Use optimal algorithms and data structures.",
        "space_complexity": "Prioritize space efficiency. Minimize memory usage.",
        "readability": "Prioritize code clarity and maintainability. Use descriptive names and clear logic.",
        "balanced": "Balance time efficiency, space efficiency, and code readability."
    }
    
    prompt += f"""
OPTIMIZATION FOCUS:
{optimization_guidance.get(optimization_target, optimization_guidance["balanced"])}
"""
    
    # Add examples if provided
    if examples:
        prompt += "\nEXAMPLES:\n"
        for i, example in enumerate(examples, 1):
            prompt += f"Example {i}:\n"
            prompt += f"  Input: {example.get('input', 'N/A')}\n"
            prompt += f"  Output: {example.get('output', 'N/A')}\n"
    
    # Add output format instructions
    prompt += f"""
REQUIREMENTS:
1. Write clean, efficient {language} code
2. Include inline comments explaining the approach
3. Use appropriate algorithmic patterns (e.g., Two Pointers, Sliding Window, Dynamic Programming)
4. Handle edge cases
5. Follow {language} best practices and naming conventions

OUTPUT FORMAT (JSON):
{{
    "code": "your complete {language} code here",
    "algorithm_used": "name of algorithm/pattern used",
    "time_complexity": "Big-O time complexity",
    "space_complexity": "Big-O space complexity",
    "explanation": "brief explanation of the approach",
    "edge_cases_handled": ["list of edge cases handled"]
}}

Generate the code now:"""
    
    return prompt


def build_generation_prompt_with_examples() -> str:
    """
    Build a few-shot prompt with examples for better results
    
    Returns:
        Prompt with example problem-solution pairs
    """
    
    prompt = """You are an expert software engineer. Here are examples of problem-solving:

EXAMPLE 1:
Problem: Find two numbers in an array that sum to a target value.
Constraints: O(n) time complexity
Language: Python

Solution:
```json
{
    "code": "def two_sum(nums, target):\\n    seen = {}\\n    for i, num in enumerate(nums):\\n        complement = target - num\\n        if complement in seen:\\n            return [seen[complement], i]\\n        seen[num] = i\\n    return []",
    "algorithm_used": "Hash Map",
    "time_complexity": "O(n)",
    "space_complexity": "O(n)",
    "explanation": "Use a hash map to store seen numbers. For each number, check if its complement exists.",
    "edge_cases_handled": ["empty array", "no solution exists", "duplicate numbers"]
}
```

EXAMPLE 2:
Problem: Find the maximum sum of a contiguous subarray.
Constraints: O(n) time complexity
Language: Python

Solution:
```json
{
    "code": "def max_subarray_sum(arr):\\n    if not arr:\\n        return 0\\n    max_sum = current_sum = arr[0]\\n    for num in arr[1:]:\\n        current_sum = max(num, current_sum + num)\\n        max_sum = max(max_sum, current_sum)\\n    return max_sum",
    "algorithm_used": "Kadane's Algorithm",
    "time_complexity": "O(n)",
    "space_complexity": "O(1)",
    "explanation": "Track current and maximum sum. At each position, decide whether to extend current subarray or start new one.",
    "edge_cases_handled": ["empty array", "all negative numbers", "single element"]
}
```

Now solve the following problem:
"""
    
    return prompt

# Made with Bob