# Efficiency Analyzer Service

A microservice that analyzes code complexity and recommends algorithmic optimizations. Part of the Algorithmic Debugging & Efficiency Coach system.

## Features

- **Time Complexity Analysis**: Calculates Big O time complexity by analyzing loops, recursion, and function calls
- **Space Complexity Analysis**: Analyzes memory usage from data structures and call stacks
- **Pattern Detection**: Identifies common inefficient patterns:
  - Nested loops (O(n²), O(n³))
  - Redundant recursion without memoization
  - Linear search in loops
  - String concatenation in loops
  - Inefficient list operations
  - Repeated sorting
- **Optimization Recommendations**: Provides specific strategies:
  - Hash Map/Set for O(1) lookups
  - Dynamic Programming for recursion
  - Two Pointers for sorted arrays
  - Sliding Window for subarrays
  - Deque for efficient queue operations
- **Performance Estimation**: Estimates speedup for different input sizes

## Architecture

- **Port**: 8002
- **Framework**: FastAPI
- **Language Support**: Python (primary), C++, Java (basic)
- **Analysis Engine**: AST-based code parsing and pattern matching

## API Endpoints

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "efficiency-analyzer",
  "version": "1.0.0"
}
```

### Analyze Code
```
POST /api/v1/analyze
```

**Request Body:**
```json
{
  "language": "python",
  "code": "def find_duplicates(arr):\n    duplicates = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j]:\n                duplicates.append(arr[i])\n    return duplicates",
  "context": "Array size can be up to 10000 elements"
}
```

**Response:**
```json
{
  "current_time_complexity": {
    "notation": "O(n²)",
    "explanation": "Quadratic time - nested iterations over the data. Contributing factors: Nested loops (2 levels): O(n²), Loop iterates n times, Loop with range iteration",
    "factors": [
      "Nested loops (2 levels): O(n²)",
      "Loop iterates n times",
      "Loop with range iteration"
    ]
  },
  "current_space_complexity": {
    "notation": "O(n)",
    "explanation": "Linear space - memory usage grows with input size. Contributing factors: List data structure(s): O(n) space",
    "factors": [
      "List data structure(s): O(n) space"
    ]
  },
  "target_time_complexity": "O(n)",
  "target_space_complexity": "O(1)",
  "inefficient_patterns": [
    {
      "pattern_type": "nested_loops",
      "severity": "medium",
      "line_numbers": [3, 4],
      "description": "Nested loops with 2 levels of nesting",
      "impact": "O(n^2) time complexity - performance degrades exponentially"
    }
  ],
  "optimization_strategies": [
    {
      "technique": "Hash Map / Set",
      "description": "Replace nested loops with hash-based lookups for O(1) access time",
      "steps": [
        "Identify the inner loop operation (usually a search or comparison)",
        "Create a hash map or set to store elements for O(1) lookup",
        "Replace inner loop with hash map lookup",
        "Reduce time complexity from O(n²) to O(n)"
      ],
      "complexity_improvement": "O(n²) → O(n)",
      "code_example": "# Before: O(n²)\nfor i in range(len(arr)):\n    for j in range(len(arr)):\n        if arr[i] == arr[j]:\n            # ...\n\n# After: O(n)\nseen = set()\nfor item in arr:\n    if item in seen:\n        # ...\n    seen.add(item)"
    }
  ],
  "estimated_improvement": {
    "n=100": "10x faster",
    "n=1000": "100x faster",
    "n=10000": "1000x faster"
  },
  "overall_score": 30
}
```

## Setup Instructions

### Local Development

1. **Install Dependencies**
   ```bash
   cd services/efficiency-analyzer
   pip install -r requirements.txt
   ```

2. **Run the Service**
   ```bash
   python -m app.main
   # Or using uvicorn directly
   uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
   ```

3. **Test the Service**
   ```bash
   curl http://localhost:8002/health
   ```

### Docker Deployment

1. **Build Image**
   ```bash
   docker build -t efficiency-analyzer:latest .
   ```

2. **Run Container**
   ```bash
   docker run -p 8002:8002 efficiency-analyzer:latest
   ```

## Example Usage

### Python Example: Nested Loops

**Input Code:**
```python
def find_pairs(arr, target):
    pairs = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == target:
                pairs.append((arr[i], arr[j]))
    return pairs
```

**Analysis Result:**
- **Current Complexity**: O(n²) time, O(n) space
- **Target Complexity**: O(n) time, O(n) space
- **Pattern Detected**: Nested loops
- **Recommendation**: Use hash map to store complements
- **Estimated Improvement**: 100x faster for n=1000

**Optimized Code:**
```python
def find_pairs(arr, target):
    seen = set()
    pairs = []
    for num in arr:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs
```

### Python Example: Redundant Recursion

**Input Code:**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Analysis Result:**
- **Current Complexity**: O(2^n) time, O(n) space
- **Target Complexity**: O(n) time, O(n) space
- **Pattern Detected**: Binary recursion without memoization
- **Recommendation**: Add memoization using @lru_cache
- **Estimated Improvement**: Exponential to linear

**Optimized Code:**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Complexity Analysis Details

### Time Complexity Detection

The service analyzes:
- **Loop Nesting**: Counts nested loop levels
- **Recursion**: Identifies recursive calls and branching factor
- **Built-in Operations**: Tracks complexity of sort(), in, etc.
- **Data Structure Operations**: Analyzes list/dict/set operations

### Space Complexity Detection

The service analyzes:
- **Data Structures**: Lists, dicts, sets created
- **Recursion Stack**: Call stack depth
- **Auxiliary Space**: Temporary variables and collections

### Pattern Detection

Common patterns identified:
1. **Nested Loops**: O(n²) or worse
2. **Redundant Recursion**: O(2^n) without memoization
3. **Linear Search in Loop**: O(n²) from nested searches
4. **String Concatenation**: O(n²) from immutability
5. **Inefficient List Ops**: O(n) operations in loops
6. **Repeated Sorting**: Multiple O(n log n) operations

## Optimization Strategies

The service recommends:
- **Hash-based Lookups**: O(1) instead of O(n)
- **Dynamic Programming**: Memoization for recursion
- **Two Pointers**: For sorted array problems
- **Sliding Window**: For subarray problems
- **Deque**: For efficient queue operations
- **Binary Search**: For sorted data
- **Sort Once**: Avoid repeated sorting

## Limitations

- **Language Support**: Full analysis only for Python; basic for C++/Java
- **Complex Algorithms**: May not detect all optimization opportunities
- **Context-Dependent**: Some optimizations depend on use case
- **Heuristic-Based**: Uses pattern matching, not formal verification

## Integration

This service integrates with:
- **Debugging Engine** (port 8001): Provides execution flow analysis
- **watsonx Integration** (port 8003): AI-powered explanations
- **Frontend** (port 3000): User interface

## Development

### Project Structure
```
services/efficiency-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models/                    # Request/response models
│   ├── services/                  # Business logic
│   ├── analyzers/                 # Complexity analyzers
│   └── utils/                     # Utilities
├── requirements.txt
├── Dockerfile
└── README.md
```

### Adding New Patterns

To add a new inefficient pattern:

1. Add detection logic in `app/analyzers/patterns.py`
2. Add optimization strategy in `app/services/optimizer.py`
3. Update pattern types in response models

### Testing

```bash
# Run with test code
curl -X POST http://localhost:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def test():\n    for i in range(n):\n        for j in range(n):\n            print(i, j)"
  }'
```

## License

Part of the IBM BOB Hackathon project.