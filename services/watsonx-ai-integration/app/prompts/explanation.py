"""
Prompt templates for AI-powered code explanation
"""

from typing import Optional, List, Dict, Any


def build_explanation_prompt(
    code: str,
    language: str,
    explanation_level: str = "beginner",
    focus_areas: Optional[List[str]] = None,
    bug_report: Optional[Dict[str, Any]] = None,
    complexity_analysis: Optional[Dict[str, Any]] = None,
    include_analogies: bool = True
) -> str:
    """
    Build a structured prompt for code explanation
    
    Args:
        code: Code to explain
        language: Programming language
        explanation_level: Target audience (beginner, intermediate, advanced)
        focus_areas: Specific areas to focus on
        bug_report: Optional bug report from debugging engine
        complexity_analysis: Optional complexity analysis
        include_analogies: Whether to include analogies
        
    Returns:
        Formatted prompt string for watsonx.ai
    """
    
    # Adjust explanation style based on level
    level_guidance = {
        "beginner": "Use simple language, avoid jargon, explain basic concepts. Assume minimal programming knowledge.",
        "intermediate": "Use standard programming terminology. Assume familiarity with basic concepts.",
        "advanced": "Use technical language. Focus on algorithmic insights and optimization techniques."
    }
    
    prompt = f"""You are an expert programming educator who excels at explaining code clearly and effectively.

TASK: Provide a comprehensive explanation of the following {language} code.

CODE TO EXPLAIN:
```{language}
{code}
```

AUDIENCE LEVEL: {explanation_level.upper()}
{level_guidance.get(explanation_level, level_guidance["beginner"])}
"""
    
    # Add bug report context if available
    if bug_report:
        prompt += "\nBUG ANALYSIS CONTEXT:\n"
        if bug_report.get("has_errors"):
            prompt += "The debugging engine has identified issues in this code:\n"
            
            if bug_report.get("syntax_errors"):
                prompt += f"- Syntax errors: {len(bug_report['syntax_errors'])} found\n"
            
            if bug_report.get("logic_errors"):
                prompt += f"- Logic errors: {len(bug_report['logic_errors'])} found\n"
                for error in bug_report.get("logic_errors", [])[:3]:  # Show first 3
                    prompt += f"  * {error.get('type', 'Unknown')}: {error.get('message', 'No details')}\n"
    
    # Add complexity analysis context if available
    if complexity_analysis:
        prompt += "\nEFFICIENCY ANALYSIS CONTEXT:\n"
        if complexity_analysis.get("time_complexity"):
            prompt += f"- Time Complexity: {complexity_analysis['time_complexity']}\n"
        if complexity_analysis.get("space_complexity"):
            prompt += f"- Space Complexity: {complexity_analysis['space_complexity']}\n"
        if complexity_analysis.get("inefficient_patterns"):
            prompt += "- Inefficient patterns detected:\n"
            for pattern in complexity_analysis.get("inefficient_patterns", [])[:3]:
                prompt += f"  * {pattern}\n"
    
    # Add focus areas if specified
    if focus_areas:
        prompt += "\nFOCUS AREAS:\n"
        focus_descriptions = {
            "bugs": "Explain what bugs exist and why they occur",
            "inefficiencies": "Explain why the code is inefficient and how it could be improved",
            "algorithm": "Explain the algorithm and approach used",
            "data_structures": "Explain the data structures used and why",
            "edge_cases": "Explain edge cases and how they're handled (or not)",
            "best_practices": "Explain adherence to or violations of best practices"
        }
        for area in focus_areas:
            description = focus_descriptions.get(area, area)
            prompt += f"- {description}\n"
    
    # Add output format
    prompt += f"""
EXPLANATION REQUIREMENTS:
1. Start with a high-level summary (2-3 sentences)
2. Provide detailed line-by-line or section-by-section explanation
3. Identify key programming concepts used
4. Point out any potential issues or bugs
5. Suggest improvements if applicable
6. Include learning resources for deeper understanding
"""
    
    if include_analogies:
        prompt += "7. Use real-world analogies to make concepts clearer\n"
    
    prompt += f"""
OUTPUT FORMAT (JSON):
{{
    "summary": "high-level summary of what the code does",
    "detailed_explanation": "comprehensive explanation of how the code works",
    "key_concepts": ["list of key programming concepts used"],
    "potential_issues": [
        {{
            "type": "issue type (e.g., bug, inefficiency, edge case)",
            "description": "what the issue is and why it matters"
        }}
    ],
    "suggestions": ["list of improvement suggestions"],
    "learning_resources": [
        {{
            "title": "resource title",
            "description": "what you'll learn",
            "relevance": "why it's relevant to this code"
        }}
    ]"""
    
    if include_analogies:
        prompt += """,
    "analogies": ["list of real-world analogies to explain concepts"]"""
    
    prompt += """
}

Provide the explanation now:"""
    
    return prompt


def build_explanation_prompt_with_examples() -> str:
    """
    Build a few-shot explanation prompt with examples
    
    Returns:
        Prompt with example explanations
    """
    
    prompt = """You are an expert programming educator. Here are examples of good code explanations:

EXAMPLE 1 - Beginner Level:

Code (Python):
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
```

Explanation:
```json
{
    "summary": "This function calculates the factorial of a number using recursion. Factorial of n (written as n!) means multiplying all positive integers from 1 to n.",
    "detailed_explanation": "The function works by calling itself with smaller numbers until it reaches 0. When n is 0, it returns 1 (base case). Otherwise, it multiplies n by the factorial of (n-1). For example, factorial(3) = 3 × factorial(2) = 3 × 2 × factorial(1) = 3 × 2 × 1 × factorial(0) = 3 × 2 × 1 × 1 = 6.",
    "key_concepts": ["recursion", "base case", "function calls", "mathematical operations"],
    "potential_issues": [
        {
            "type": "missing_validation",
            "description": "The function doesn't check if n is negative. Negative numbers would cause infinite recursion and crash the program."
        },
        {
            "type": "stack_overflow",
            "description": "For very large numbers (e.g., n > 1000), the function might exceed Python's recursion limit and crash."
        }
    ],
    "suggestions": [
        "Add input validation: check if n is negative and handle it appropriately",
        "Consider using an iterative approach for large numbers to avoid stack overflow",
        "Add a docstring to explain what the function does"
    ],
    "learning_resources": [
        {
            "title": "Understanding Recursion",
            "description": "Learn how functions can call themselves and when to use recursion",
            "relevance": "This code uses recursion as its core technique"
        }
    ],
    "analogies": [
        "Think of recursion like Russian nesting dolls. Each doll contains a smaller version of itself until you reach the smallest one (base case). Similarly, factorial(n) contains factorial(n-1), which contains factorial(n-2), until you reach factorial(0)."
    ]
}
```

Now explain the following code:
"""
    
    return prompt

# Made with Bob