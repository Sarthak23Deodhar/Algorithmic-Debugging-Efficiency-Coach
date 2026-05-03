
# API Reference

Complete API documentation for all microservices in the Algorithmic Debugging & Efficiency Coach system.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Common Patterns](#common-patterns)
4. [Debugging Engine API](#debugging-engine-api)
5. [Efficiency Analyzer API](#efficiency-analyzer-api)
6. [watsonx.ai Integration API](#watsonxai-integration-api)
7. [watsonx Orchestrate API](#watsonx-orchestrate-api)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

## Overview

### Base URLs

| Service | Base URL | Port |
|---------|----------|------|
| Debugging Engine | `http://localhost:8001` | 8001 |
| Efficiency Analyzer | `http://localhost:8002` | 8002 |
| watsonx.ai Integration | `http://localhost:8003` | 8003 |
| watsonx Orchestrate | `http://localhost:8004` | 8004 |

### Supported Languages

All services support the following programming languages:
- `python` - Python 3.x
- `cpp` - C++11 and later
- `java` - Java 8 and later

### Content Type

All requests must use `Content-Type: application/json`

### Response Format

All responses are in JSON format with the following structure:

```json
{
  "status": "success|error",
  "data": { ... },
  "message": "Optional message",
  "timestamp": "ISO-8601 timestamp"
}
```

## Authentication

### Development Environment

No authentication required for local development.

### Production Environment

Production deployments use IBM Cloud IAM authentication:

```bash
Authorization: Bearer <IAM_TOKEN>
```

To obtain an IAM token:

```bash
curl -X POST "https://iam.cloud.ibm.com/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=<YOUR_API_KEY>"
```

## Common Patterns

### Request Structure

```json
{
  "code": "string (required) - Source code to analyze",
  "language": "string (required) - python|cpp|java",
  "options": {
    "key": "value (optional) - Service-specific options"
  }
}
```

### Response Structure

```json
{
  "status": "success",
  "data": {
    "analysis_id": "uuid",
    "results": { ... }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

## Debugging Engine API

Base URL: `http://localhost:8001`

### Health Check

Check service health status.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "debugging-engine",
  "version": "1.0.0",
  "timestamp": "2026-05-02T10:30:00Z"
}
```

**Example**:
```bash
curl http://localhost:8001/health
```

---

### Analyze Code

Submit code for debugging analysis.

**Endpoint**: `POST /api/v1/analyze`

**Request Body**:
```json
{
  "code": "def hello():\n    print(\"Hello\"",
  "language": "python"
}
```

**Parameters**:
- `code` (string, required): Source code to analyze
- `language` (string, required): Programming language (`python`, `cpp`, `java`)

**Response**:
```json
{
  "status": "success",
  "data": {
    "bugs": [
      {
        "type": "syntax_error",
        "severity": "critical",
        "line": 1,
        "column": 25,
        "message": "Missing closing parenthesis",
        "suggestion": "Add ')' at the end of line 1"
      }
    ],
    "execution_flow": [
      {
        "step": 1,
        "line": 1,
        "action": "function_definition",
        "description": "Define function 'hello'"
      }
    ],
    "explanation": "The code has a syntax error on line 1. The print statement is missing a closing parenthesis, which will prevent the code from executing.",
    "bug_count": 1,
    "severity_summary": {
      "critical": 1,
      "high": 0,
      "medium": 0,
      "low": 0
    }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

**Bug Object Fields**:
- `type`: Bug category (syntax_error, logic_error, runtime_error, etc.)
- `severity`: critical, high, medium, low
- `line`: Line number where bug occurs
- `column`: Column number (if available)
- `message`: Description of the bug
- `suggestion`: Recommended fix

**Example**:
```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
    "language": "python"
  }'
```

**Status Codes**:
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request parameters
- `422 Unprocessable Entity`: Code cannot be parsed
- `500 Internal Server Error`: Server error

---

## Efficiency Analyzer API

Base URL: `http://localhost:8002`

### Health Check

Check service health status.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "efficiency-analyzer",
  "version": "1.0.0",
  "timestamp": "2026-05-02T10:30:00Z"
}
```

---

### Analyze Efficiency

Submit code for complexity and efficiency analysis.

**Endpoint**: `POST /api/v1/analyze`

**Request Body**:
```json
{
  "code": "def find_pair(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return (i, j)\n    return None",
  "language": "python"
}
```

**Parameters**:
- `code` (string, required): Source code to analyze
- `language` (string, required): Programming language

**Response**:
```json
{
  "status": "success",
  "data": {
    "time_complexity": {
      "current": "O(n²)",
      "target": "O(n)",
      "explanation": "The nested loops iterate through all pairs of elements, resulting in quadratic time complexity."
    },
    "space_complexity": {
      "current": "O(1)",
      "target": "O(n)",
      "explanation": "Current implementation uses constant space. Optimization to O(n) time requires O(n) space for a hash map."
    },
    "patterns": [
      {
        "name": "nested_loops",
        "description": "Nested loops checking all pairs",
        "line_start": 2,
        "line_end": 5,
        "impact": "high",
        "suggestion": "Use hash map for O(1) lookups"
      }
    ],
    "recommended_strategy": "Hash Map / Set",
    "optimization_steps": [
      {
        "step": 1,
        "title": "Use Hash Map for Complement Lookup",
        "description": "Instead of nested loops, use a hash map to store seen numbers and check for complements in O(1) time.",
        "complexity_improvement": "O(n²) → O(n)"
      },
      {
        "step": 2,
        "title": "Single Pass Solution",
        "description": "Iterate through the array once, checking if the complement (target - current) exists in the hash map.",
        "code_example": "seen = {}\nfor i, num in enumerate(nums):\n    complement = target - num\n    if complement in seen:\n        return (seen[complement], i)\n    seen[num] = i"
      }
    ],
    "performance_metrics": {
      "estimated_speedup": "100x for n=1000",
      "memory_tradeoff": "O(n) additional space"
    }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

**Pattern Object Fields**:
- `name`: Pattern identifier
- `description`: What the pattern does
- `line_start`: Starting line number
- `line_end`: Ending line number
- `impact`: high, medium, low
- `suggestion`: How to optimize

**Example**:
```bash
curl -X POST http://localhost:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
    "language": "python"
  }'
```

**Status Codes**:
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request parameters
- `422 Unprocessable Entity`: Code cannot be analyzed
- `500 Internal Server Error`: Server error

---

## watsonx.ai Integration API

Base URL: `http://localhost:8003`

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "watsonx-ai-integration",
  "version": "1.0.0",
  "watsonx_connected": true,
  "timestamp": "2026-05-02T10:30:00Z"
}
```

---

### Refactor Code

Generate refactored and optimized code.

**Endpoint**: `POST /api/v1/refactor`

**Request Body**:
```json
{
  "code": "def find_duplicates(nums):\n    result = []\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] == nums[j] and nums[i] not in result:\n                result.append(nums[i])\n    return result",
  "language": "python",
  "bugs": [],
  "optimization_strategy": "Use set for O(1) lookups"
}
```

**Parameters**:
- `code` (string, required): Original source code
- `language` (string, required): Programming language
- `bugs` (array, optional): List of bugs from debugging analysis
- `optimization_strategy` (string, optional): Recommended optimization approach

**Response**:
```json
{
  "status": "success",
  "data": {
    "refactored_code": "def find_duplicates(nums):\n    \"\"\"Find duplicate numbers using set for O(n) complexity.\"\"\"\n    seen = set()\n    duplicates = set()\n    \n    for num in nums:\n        if num in seen:\n            duplicates.add(num)\n        else:\n            seen.add(num)\n    \n    return list(duplicates)",
    "explanation": "The refactored code uses two sets to track seen numbers and duplicates. This reduces time complexity from O(n²) to O(n) by using O(1) set lookups instead of nested loops. Space complexity increases from O(k) to O(n) where k is the number of duplicates.",
    "improvements": [
      "Reduced time complexity from O(n²) to O(n)",
      "Eliminated nested loops",
      "Used set for O(1) membership testing",
      "Added docstring for clarity"
    ],
    "complexity_change": {
      "time": {
        "before": "O(n²)",
        "after": "O(n)"
      },
      "space": {
        "before": "O(k)",
        "after": "O(n)"
      }
    }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

**Example**:
```bash
curl -X POST http://localhost:8003/api/v1/refactor \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def slow_function(n):\n    result = []\n    for i in range(n):\n        for j in range(n):\n            result.append(i*j)\n    return result",
    "language": "python",
    "bugs": [],
    "optimization_strategy": "Reduce nested loops"
  }'
```

---

### Generate Explanation

Generate plain-language explanation of code and issues.

**Endpoint**: `POST /api/v1/explain`

**Request Body**:
```json
{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "language": "python",
  "bugs": [],
  "complexity": {
    "time_complexity": {
      "current": "O(2^n)",
      "target": "O(n)"
    }
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "explanation": "This is a recursive implementation of the Fibonacci sequence. While correct, it has exponential time complexity O(2^n) because it recalculates the same values multiple times. For example, fib(5) calls fib(4) and fib(3), but fib(4) also calls fib(3), leading to redundant calculations.\n\nTo optimize this to O(n) time complexity, you can use memoization (caching previously calculated values) or dynamic programming (bottom-up approach). This trades space for time, using O(n) memory to achieve O(n) time.",
    "key_points": [
      "Recursive implementation is correct but inefficient",
      "Exponential time complexity due to redundant calculations",
      "Can be optimized using memoization or dynamic programming",
      "Optimization trades space (O(n)) for time (O(2^n) → O(n))"
    ],
    "learning_resources": [
      "Dynamic Programming fundamentals",
      "Memoization techniques",
      "Time-space tradeoffs"
    ]
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

---

### Generate Code

Generate code from natural language description.

**Endpoint**: `POST /api/v1/generate`

**Request Body**:
```json
{
  "description": "Write a function that finds the longest substring without repeating characters",
  "language": "python",
  "constraints": {
    "time_complexity": "O(n)",
    "space_complexity": "O(min(n, m))"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "generated_code": "def longest_substring_without_repeating(s: str) -> int:\n    \"\"\"\n    Find the length of the longest substring without repeating characters.\n    Time: O(n), Space: O(min(n, m)) where m is charset size\n    \"\"\"\n    char_index = {}\n    max_length = 0\n    start = 0\n    \n    for end, char in enumerate(s):\n        if char in char_index and char_index[char] >= start:\n            start = char_index[char] + 1\n        \n        char_index[char] = end\n        max_length = max(max_length, end - start + 1)\n    \n    return max_length",
    "explanation": "This solution uses a sliding window approach with a hash map to track character positions. It maintains a window of unique characters and expands/contracts it as needed.",
    "complexity": {
      "time": "O(n)",
      "space": "O(min(n, m))"
    }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

---

## watsonx Orchestrate API

Base URL: `http://localhost:8004`

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "watsonx-orchestrate-integration",
  "version": "1.0.0",
  "orchestrate_connected": true,
  "timestamp": "2026-05-02T10:30:00Z"
}
```

---

### Trigger Automation

Trigger automated workflows for documentation, tickets, and learning paths.

**Endpoint**: `POST /api/v1/automate`

**Request Body**:
```json
{
  "code": "def example(): pass",
  "language": "python",
  "analysis_results": {
    "debugging": {
      "bugs": [
        {
          "type": "logic_error",
          "severity": "medium",
          "message": "Potential issue"
        }
      ]
    },
    "efficiency": {
      "time_complexity": {
        "current": "O(n²)",
        "target": "O(n)"
      }
    }
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "documentation": {
      "status": "success",
      "files": [
        "docs/analysis_report_20260502.md",
        "docs/optimization_guide_20260502.md"
      ],
      "summary": "Generated technical documentation with analysis results and optimization recommendations"
    },
    "tickets": {
      "status": "success",
      "ticket_ids": [
        "TECH-1234",
        "TECH-1235"
      ],
      "details": [
        {
          "id": "TECH-1234",
          "title": "Optimize algorithm complexity from O(n²) to O(n)",
          "priority": "medium",
          "url": "https://jira.example.com/browse/TECH-1234"
        }
      ]
    },
    "learning_path": {
      "status": "success",
      "topics": [
        "Hash Maps and Sets",
        "Time Complexity Analysis",
        "Algorithm Optimization Techniques",
        "Dynamic Programming Basics"
      ],
      "resources": [
        {
          "topic": "Hash Maps and Sets",
          "resources": [
            "Introduction to Hash Tables",
            "Set Operations in Python"
          ]
        }
      ]
    }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

---

### Generate Documentation

Generate technical documentation from analysis results.

**Endpoint**: `POST /api/v1/documentation`

**Request Body**:
```json
{
  "code": "def example(): pass",
  "analysis_results": { ... },
  "format": "markdown"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "documentation": "# Code Analysis Report\n\n## Summary\n...",
    "file_path": "docs/analysis_report_20260502.md",
    "format": "markdown"
  }
}
```

---

### Create Tickets

Create tickets in issue tracking system.

**Endpoint**: `POST /api/v1/tickets`

**Request Body**:
```json
{
  "issues": [
    {
      "title": "Optimize algorithm",
      "description": "Current O(n²), target O(n)",
      "priority": "medium"
    }
  ]
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "tickets": [
      {
        "id": "TECH-1234",
        "title": "Optimize algorithm",
        "url": "https://jira.example.com/browse/TECH-1234"
      }
    ]
  }
}
```

---

### Generate Learning Path

Generate personalized learning path based on analysis.

**Endpoint**: `POST /api/v1/learning-path`

**Request Body**:
```json
{
  "analysis_results": {
    "patterns": ["nested_loops", "inefficient_search"],
    "complexity": "O(n²)"
  },
  "user_level": "intermediate"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "topics": [
      "Hash Maps and Sets",
      "Algorithm Complexity",
      "Optimization Techniques"
    ],
    "resources": [ ... ],
    "estimated_time": "4-6 hours"
  }
}
```

---

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_LANGUAGE",
    "message": "Unsupported language: javascript",
    "details": {
      "supported_languages": ["python", "cpp", "java"]
    }
  },
  "timestamp": "2026-05-02T10:30:00Z"
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_REQUEST` | Malformed request body | 400 |
| `INVALID_LANGUAGE` | Unsupported programming language | 400 |
| `INVALID_CODE` | Code cannot be parsed | 422 |
| `MISSING_PARAMETER` | Required parameter missing | 400 |
| `ANALYSIS_FAILED` | Analysis could not be completed | 500 |
| `WATSONX_ERROR` | Error communicating with watsonx | 503 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `AUTHENTICATION_FAILED` | Invalid or missing credentials | 401 |
| `AUTHORIZATION_FAILED` | Insufficient permissions | 403 |

## Rate Limiting

### Development Environment

No rate limiting in local development.

### Production Environment

Rate limits apply per API key:

| Tier | Requests/Hour | Requests/Day |
|------|---------------|--------------|
| Free | 10 | 100 |
| Pro | 100 | 1,000 |
| Enterprise | Unlimited | Unlimited |

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1651478400
```

### Rate Limit Exceeded Response

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 3600 seconds.",
    "details": {
      "limit": 100,
      "reset_at": "2026-05-02T11:00:00Z"
    }
  }
}
```

## Examples

### Complete Analysis Workflow

```python
import requests

BASE_URLS = {
    "debugging": "http://localhost:8001",
    "efficiency": "http://localhost:8002",
    "watsonx_ai": "http://localhost:8003",
    "watsonx_orchestrate": "http://localhost:8004"
}

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
debug_response = requests.post(
    f"{BASE_URLS['debugging']}/api/v1/analyze",
    json={"code": code, "language": "python"}
)
debug_data = debug_response.json()["data"]

# Step 2: Efficiency analysis
efficiency_response = requests.post(
    f"{BASE_URLS['efficiency']}/api/v1/analyze",
    json={"code": code, "language": "python"}
)
efficiency_data = efficiency_response.json()["data"]

# Step 3: Get refactored code
refactor_response = requests.post(
    f"{BASE_URLS['watsonx_ai']}/api/v1/refactor",
    json={
        "code": code,
        "language": "python",
        "bugs": debug_data["bugs"],
        "optimization_strategy": efficiency_data["recommended_strategy"]
    }
)
refactor_data = refactor_response.json()["data"]

# Step 4: Trigger automation
automation_response = requests.post(
    f"{BASE_URLS['watsonx_orchestrate']}/api/v1/automate",
    json={
        "code": code,
        "language": "python",
        "analysis_results": {
            "debugging": debug_data,
            "efficiency": efficiency_data
        }
    }
)
automation_data = automation_response.json()["data"]

print("Analysis complete!")
print(f"Bugs: {len(debug_data['bugs'])}")
print(f"Complexity: {efficiency_data['time_complexity']['current']}")
print(f"Tickets created: {automation_data['tickets']['ticket_ids']}")
```

---

For more examples and integration guides, see the [Getting Started Guide](GETTING_STARTED.md).
