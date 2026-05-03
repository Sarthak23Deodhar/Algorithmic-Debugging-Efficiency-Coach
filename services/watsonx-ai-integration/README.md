# watsonx.ai Integration Service

AI-powered code generation, refactoring, and explanation service using IBM watsonx.ai.

## Overview

This service integrates with IBM watsonx.ai to provide intelligent code operations:
- **Code Generation**: Generate optimized code from natural language descriptions
- **Code Refactoring**: Optimize existing code while preserving functionality
- **Code Explanation**: Generate educational explanations of code with analogies

## Architecture

The service is built as a serverless function using FastAPI and integrates with:
- **IBM watsonx.ai**: Primary AI engine using granite-20b-code-instruct model
- **Debugging Engine** (port 8001): Provides bug reports for context
- **Efficiency Analyzer** (port 8002): Provides complexity analysis for context

### Key Components

```
watsonx-ai-integration/
├── app/
│   ├── handler.py              # FastAPI application & endpoints
│   ├── models/                 # Request/response models
│   ├── services/               # Core services
│   │   ├── watsonx_client.py   # watsonx.ai API client (with mock mode)
│   │   ├── code_generator.py   # Code generation service
│   │   ├── refactoring.py      # Code refactoring service
│   │   └── explainer.py        # Code explanation service
│   ├── prompts/                # Prompt templates
│   └── utils/                  # Utilities
```

## watsonx.ai Integration Details

### Models Used

- **Primary Model**: `ibm/granite-20b-code-instruct`
  - Used for: Complex code generation, refactoring
  - Temperature: 0.2-0.7 depending on task
  - Max tokens: 2048

- **Fast Model**: `ibm/granite-8b-code-base`
  - Used for: Simple explanations, quick tasks
  - Temperature: 0.4-0.8
  - Max tokens: 1024

### Prompt Engineering

The service uses structured prompts with:
- Few-shot examples for better results
- Explicit formatting instructions (JSON output)
- Context from debugging and efficiency analysis
- Audience-level adaptation (beginner/intermediate/advanced)

## API Documentation

### Base URL
```
http://localhost:8003
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "watsonx-ai-integration",
  "version": "1.0.0",
  "watsonx_connected": true,
  "mock_mode": true
}
```

#### 2. Generate Code
```http
POST /generate
```

**Request Body:**
```json
{
  "problem_description": "Find all pairs in an array that sum to a target value",
  "language": "python",
  "constraints": "Must be O(n) time complexity",
  "optimization_target": "time_complexity",
  "include_comments": true,
  "examples": [
    {
      "input": "[2, 7, 11, 15], target=9",
      "output": "[(0, 1)]"
    }
  ]
}
```

**Response:**
```json
{
  "job_id": "gen_abc123",
  "status": "completed",
  "operation_type": "generate",
  "generated_code": {
    "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
    "language": "python",
    "algorithm_used": "Hash Map",
    "complexity_analysis": {
      "time": "O(n)",
      "space": "O(n)"
    },
    "explanation": "Uses a hash map to store seen numbers...",
    "test_cases": [...]
  },
  "confidence_score": 0.95,
  "processing_time_ms": 1250.5,
  "model_used": "ibm/granite-20b-code-instruct",
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:01Z"
}
```

#### 3. Refactor Code
```http
POST /refactor
```

**Request Body:**
```json
{
  "original_code": "def find_duplicates(arr):\n    duplicates = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j]:\n                duplicates.append(arr[i])\n    return duplicates",
  "language": "python",
  "inefficient_patterns": ["nested_loops", "O(n^2)_time"],
  "target_complexity": "O(n) time",
  "optimization_focus": "time_complexity",
  "include_explanation": true
}
```

**Response:**
```json
{
  "job_id": "ref_xyz789",
  "status": "completed",
  "operation_type": "refactor",
  "refactored_code": {
    "original_code": "...",
    "refactored_code": "def find_duplicates(arr):\n    seen = set()\n    duplicates = set()\n    for num in arr:\n        if num in seen:\n            duplicates.add(num)\n        seen.add(num)\n    return list(duplicates)",
    "changes_made": [
      "Replaced nested loops with single pass",
      "Used hash set for O(1) lookups"
    ],
    "complexity_improvement": {
      "before": {"time": "O(n²)", "space": "O(k)"},
      "after": {"time": "O(n)", "space": "O(n)"}
    },
    "diff": "...",
    "explanation": "Replaced O(n²) nested loop approach..."
  },
  "confidence_score": 0.92,
  "processing_time_ms": 1450.2,
  "model_used": "ibm/granite-20b-code-instruct"
}
```

#### 4. Explain Code
```http
POST /explain
```

**Request Body:**
```json
{
  "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
  "language": "python",
  "explanation_level": "beginner",
  "focus_areas": ["algorithm", "recursion"],
  "include_analogies": true,
  "bug_report": {
    "has_errors": false,
    "logic_errors": [...]
  },
  "complexity_analysis": {
    "time_complexity": "O(n)",
    "space_complexity": "O(n)"
  }
}
```

**Response:**
```json
{
  "job_id": "exp_def456",
  "status": "completed",
  "operation_type": "explain",
  "explanation": {
    "summary": "This function calculates factorial using recursion...",
    "detailed_explanation": "The function works by calling itself...",
    "key_concepts": ["recursion", "base case", "call stack"],
    "potential_issues": [
      {
        "type": "missing_validation",
        "description": "No check for negative numbers"
      }
    ],
    "suggestions": [
      "Add input validation",
      "Consider iterative approach for large values"
    ],
    "learning_resources": [...],
    "analogies": [
      "Think of recursion like Russian nesting dolls..."
    ]
  },
  "confidence_score": 0.88,
  "processing_time_ms": 980.3
}
```

#### 5. Get Job Status
```http
GET /jobs/{job_id}
```

#### 6. Cancel Job
```http
DELETE /jobs/{job_id}
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Docker (optional)
- IBM watsonx.ai API credentials (for production)

### Environment Variables

Create a `.env` file:
```bash
# watsonx.ai Configuration
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_API_URL=https://us-south.ml.cloud.ibm.com

# Service Configuration
PORT=8003
MOCK_MODE=true  # Set to false for production

# Optional
LOG_LEVEL=INFO
```

### Local Development

1. **Install dependencies:**
```bash
cd services/watsonx-ai-integration
pip install -r requirements.txt
```

2. **Run the service:**
```bash
python -m app.handler
```

3. **Access the API:**
- Service: http://localhost:8003
- API Docs: http://localhost:8003/docs
- Health: http://localhost:8003/health

### Docker Deployment

1. **Build the image:**
```bash
docker build -t watsonx-ai-integration:latest .
```

2. **Run the container:**
```bash
docker run -p 8003:8003 \
  -e WATSONX_API_KEY=your_key \
  -e WATSONX_PROJECT_ID=your_project \
  -e MOCK_MODE=false \
  watsonx-ai-integration:latest
```

## Mock Mode

The service includes a **mock mode** for development without watsonx.ai credentials:

- Simulates API latency (500-1500ms)
- Returns plausible responses based on prompt analysis
- Useful for testing integration and UI development
- Enable with `MOCK_MODE=true` (default)

### Mock Response Examples

**Code Generation:**
- Detects "two sum" → Returns hash map solution
- Generic problems → Returns template code

**Refactoring:**
- Returns optimized version with hash set pattern
- Includes complexity improvements

**Explanation:**
- Returns structured explanation with concepts and suggestions

## Performance Benchmarks

### Mock Mode
- Code Generation: ~500-1500ms
- Refactoring: ~600-1200ms
- Explanation: ~400-1000ms

### Real API (Expected)
- Code Generation: ~2000-4000ms
- Refactoring: ~2500-4500ms
- Explanation: ~1500-3000ms

## Model Selection Guide

| Task | Complexity | Model | Temperature |
|------|-----------|-------|-------------|
| Simple explanation | Low | granite-8b | 0.6-0.8 |
| Code generation | Medium | granite-20b | 0.5-0.7 |
| Complex refactoring | High | granite-20b | 0.2-0.3 |
| Beginner explanation | Low | granite-8b | 0.8 |
| Advanced explanation | High | granite-20b | 0.4 |

## Integration with Other Services

### With Debugging Engine
```python
# Get bug report from debugging engine
bug_report = requests.post("http://localhost:8001/analyze", json={...}).json()

# Request explanation with bug context
explanation = requests.post("http://localhost:8003/explain", json={
    "code": code,
    "language": "python",
    "bug_report": bug_report,
    "focus_areas": ["bugs"]
}).json()
```

### With Efficiency Analyzer
```python
# Get complexity analysis
analysis = requests.post("http://localhost:8002/analyze", json={...}).json()

# Request refactoring with analysis context
refactored = requests.post("http://localhost:8003/refactor", json={
    "original_code": code,
    "language": "python",
    "inefficient_patterns": analysis["inefficient_patterns"],
    "target_complexity": "O(n)"
}).json()
```

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Limitations

### Current Implementation
- In-memory job storage (use Redis for production)
- Synchronous processing (can be made async with webhooks)
- Basic syntax validation only
- Mock mode for development

### Production Considerations
- Implement persistent job storage (Redis/PostgreSQL)
- Add rate limiting and authentication
- Implement webhook callbacks for long-running jobs
- Add comprehensive error handling and retries
- Monitor API usage and costs
- Implement caching for common requests

## Troubleshooting

### Common Issues

1. **Service won't start:**
   - Check port 8003 is available
   - Verify Python version (3.11+)
   - Check all dependencies installed

2. **Mock mode not working:**
   - Ensure `MOCK_MODE=true` in environment
   - Check logs for initialization messages

3. **Real API errors:**
   - Verify watsonx.ai credentials
   - Check API key permissions
   - Ensure project ID is correct
   - Check network connectivity

## Contributing

When adding new features:
1. Update prompt templates in `app/prompts/`
2. Add corresponding service methods
3. Update API documentation
4. Add tests
5. Update this README

## License

Made with Bob

## Support

For issues or questions:
- Check logs: Service logs to stdout
- Review API docs: http://localhost:8003/docs
- Check architecture: See `ARCHITECTURE.md`

---

**Service Status:** ✅ Operational (Mock Mode)  
**Port:** 8003  
**Version:** 1.0.0