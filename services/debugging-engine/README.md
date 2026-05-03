# Debugging Engine Service

The Debugging Engine is a core microservice of the Algorithmic Debugging & Efficiency Coach system. It analyzes code submissions in Python, C++, and Java to identify bugs, trace execution flow, and provide plain-language explanations.

## Features

- **Multi-Language Support**: Analyzes Python, C++, and Java code
- **Syntax Error Detection**: Identifies syntax errors with precise line numbers
- **Logic Error Detection**: Finds common logic errors (infinite loops, null pointers, type mismatches)
- **Execution Flow Analysis**: Maps code execution paths and control flow
- **Root Cause Analysis**: Identifies underlying causes of bugs with confidence scores
- **Plain-Language Explanations**: Converts technical errors into beginner-friendly explanations

## Architecture

The service is built with:
- **FastAPI**: High-performance async web framework
- **Python 3.11**: Modern Python with type hints
- **Tree-sitter**: Multi-language code parsing
- **Static Analysis Tools**: pylint (Python), clang (C++), javac (Java)

## API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "debugging-engine",
  "version": "1.0.0"
}
```

### Debug Code
```http
POST /api/v1/debug
Content-Type: application/json
```

**Request Body:**
```json
{
  "language": "python",
  "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
  "context": "Calculate factorial of a number"
}
```

**Response:**
```json
{
  "has_errors": false,
  "syntax_errors": [],
  "logic_errors": [],
  "execution_flow": {
    "entry_point": "module_level",
    "functions": [
      {
        "name": "factorial",
        "line": 1,
        "end_line": 4,
        "params": ["n"]
      }
    ],
    "control_structures": [
      {
        "type": "if",
        "line": 2,
        "end_line": 3
      }
    ],
    "call_graph": {
      "factorial": []
    },
    "unreachable_code": []
  },
  "root_causes": [],
  "explanations": [],
  "analysis_time_ms": 45.2
}
```

## Setup Instructions

### Local Development

1. **Install Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Install Dependencies**
   ```bash
   cd services/debugging-engine
   pip install -r requirements.txt
   ```

3. **Install System Tools (Optional but Recommended)**
   
   For full functionality, install language-specific tools:
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y clang clang-tools default-jdk
   ```
   
   **macOS:**
   ```bash
   brew install llvm openjdk
   ```
   
   **Windows:**
   - Install LLVM from https://releases.llvm.org/
   - Install JDK from https://adoptium.net/

4. **Run the Service**
   ```bash
   python -m app.main
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

5. **Access API Documentation**
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

### Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t debugging-engine:latest .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name debugging-engine \
     -p 8001:8001 \
     debugging-engine:latest
   ```

3. **Check Logs**
   ```bash
   docker logs -f debugging-engine
   ```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debugging-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: debugging-engine
  template:
    metadata:
      labels:
        app: debugging-engine
    spec:
      containers:
      - name: debugging-engine
        image: debugging-engine:latest
        ports:
        - containerPort: 8001
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 10
          periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: debugging-engine
spec:
  selector:
    app: debugging-engine
  ports:
  - port: 8001
    targetPort: 8001
  type: ClusterIP
```

## Example Usage

### Python Code Analysis

```python
import requests

code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
"""

response = requests.post(
    "http://localhost:8001/api/v1/debug",
    json={
        "language": "python",
        "code": code,
        "context": "Division function"
    }
)

print(response.json())
```

### C++ Code Analysis

```python
cpp_code = """
#include <iostream>

int main() {
    int x = 10
    std::cout << x << std::endl;
    return 0;
}
"""

response = requests.post(
    "http://localhost:8001/api/v1/debug",
    json={
        "language": "cpp",
        "code": cpp_code
    }
)

print(response.json())
```

### Java Code Analysis

```python
java_code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!")
    }
}
"""

response = requests.post(
    "http://localhost:8001/api/v1/debug",
    json={
        "language": "java",
        "code": java_code
    }
)

print(response.json())
```

## Project Structure

```
services/debugging-engine/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py             # Request models
│   │   └── response.py            # Response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── execution_flow.py      # Execution flow analyzer
│   │   ├── root_cause.py          # Root cause identifier
│   │   └── explainer.py           # Bug explainer
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── python_parser.py       # Python AST parser
│   │   ├── cpp_parser.py          # C++ tree-sitter parser
│   │   └── java_parser.py         # Java tree-sitter parser
│   └── utils/
│       ├── __init__.py
│       └── logger.py              # Logging configuration
├── requirements.txt
├── Dockerfile
└── README.md
```

## Configuration

### Environment Variables

- `PORT`: Service port (default: 8001)
- `LOG_LEVEL`: Logging level (default: INFO)
- `PYTHONUNBUFFERED`: Disable Python output buffering (default: 1)

## Performance

- **Average Analysis Time**: 50-200ms per submission
- **Supported Code Size**: Up to 50,000 characters
- **Concurrent Requests**: Handles multiple requests via async processing
- **Resource Usage**: 2 CPU cores, 4GB RAM recommended

## Limitations

1. **Static Analysis Only**: Does not execute code for security reasons
2. **Language-Specific Tools**: Full functionality requires external tools (pylint, clang, javac)
3. **Simplified Logic Detection**: Advanced logic errors may not be detected
4. **No Runtime Analysis**: Cannot detect runtime-specific issues

## Future Enhancements

- [ ] Integration with watsonx.ai for AI-powered explanations
- [ ] Support for additional languages (Go, Rust, JavaScript)
- [ ] Advanced control flow analysis
- [ ] Memory leak detection for C++
- [ ] Performance profiling integration
- [ ] Code fix suggestions with diffs

## Troubleshooting

### Issue: "Pylint not found"
**Solution**: Install pylint: `pip install pylint`

### Issue: "Clang not found"
**Solution**: Install LLVM/Clang for your platform

### Issue: "Tree-sitter parsing fails"
**Solution**: Ensure tree-sitter and language grammars are installed correctly

### Issue: "Port 8001 already in use"
**Solution**: Change port with `--port` flag or stop conflicting service

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write docstrings for public APIs
4. Test with all three supported languages
5. Update README for new features

## License

Copyright © 2026 IBM. All rights reserved.

## Support

For issues and questions:
- GitHub Issues: [Project Repository]
- Email: support@algo-coach.ibm.cloud
- Documentation: https://docs.algo-coach.ibm.cloud

## Version History

- **1.0.0** (2026-05-01): Initial release
  - Multi-language support (Python, C++, Java)
  - Syntax and logic error detection
  - Execution flow analysis
  - Plain-language explanations