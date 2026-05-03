
# Getting Started Guide

Welcome to the Algorithmic Debugging & Efficiency Coach! This guide will help you set up and start using the system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Running Services](#running-services)
5. [Using the CLI Demo](#using-the-cli-demo)
6. [Example Workflows](#example-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

## Prerequisites

### Required Software

- **Python 3.11 or higher**
  ```bash
  python --version  # Should be 3.11+
  ```

- **Docker & Docker Compose** (for containerized deployment)
  ```bash
  docker --version
  docker-compose --version
  ```

- **Git** (for cloning the repository)
  ```bash
  git --version
  ```

### Optional Software

- **Kubernetes** (kubectl and minikube/kind for local K8s)
- **Node.js 18+** (for future frontend development)
- **PostgreSQL 15+** (if running without Docker)
- **Redis 7+** (if running without Docker)

### System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: Minimum 8GB, recommended 16GB
- **Disk Space**: 10GB free space
- **Network**: Internet connection for IBM watsonx services

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd algo-coach
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# IBM watsonx Configuration
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=algo_coach
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Service Ports
DEBUGGING_ENGINE_PORT=8001
EFFICIENCY_ANALYZER_PORT=8002
WATSONX_AI_PORT=8003
WATSONX_ORCHESTRATE_PORT=8004

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Step 3: Install Dependencies

#### For Individual Services

```bash
# Debugging Engine
cd services/debugging-engine
pip install -r requirements.txt

# Efficiency Analyzer
cd ../efficiency-analyzer
pip install -r requirements.txt

# watsonx.ai Integration
cd ../watsonx-ai-integration
pip install -r requirements.txt

# watsonx Orchestrate Integration
cd ../watsonx-orchestrate-integration
pip install -r requirements.txt
```

#### For CLI Demo

```bash
cd demo/cli-demo
pip install -r requirements.txt
```

## Quick Start

### Option 1: Using Docker Compose (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Option 2: Running Services Individually

Start each service in a separate terminal:

```bash
# Terminal 1: Debugging Engine
cd services/debugging-engine
python -m app.main

# Terminal 2: Efficiency Analyzer
cd services/efficiency-analyzer
python -m app.main

# Terminal 3: watsonx.ai Integration
cd services/watsonx-ai-integration
python -m app.handler

# Terminal 4: watsonx Orchestrate Integration
cd services/watsonx-orchestrate-integration
python -m app.handler
```

### Verify Services are Running

Check that all services are healthy:

```bash
# Debugging Engine
curl http://localhost:8001/health

# Efficiency Analyzer
curl http://localhost:8002/health

# watsonx.ai Integration
curl http://localhost:8003/health

# watsonx Orchestrate Integration
curl http://localhost:8004/health
```

Expected response for each:
```json
{
  "status": "healthy",
  "service": "service-name",
  "version": "1.0.0"
}
```

## Running Services

### Debugging Engine (Port 8001)

```bash
cd services/debugging-engine
python -m app.main
```

**Features**:
- Bug detection and analysis
- Execution flow visualization
- Plain-language explanations

**Test the service**:
```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello\"",
    "language": "python"
  }'
```

### Efficiency Analyzer (Port 8002)

```bash
cd services/efficiency-analyzer
python -m app.main
```

**Features**:
- Time/space complexity calculation
- Pattern detection
- Optimization recommendations

**Test the service**:
```bash
curl -X POST http://localhost:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def find_pair(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return (i, j)\n    return None",
    "language": "python"
  }'
```

### watsonx.ai Integration (Port 8003)

```bash
cd services/watsonx-ai-integration
python -m app.handler
```

**Features**:
- Code refactoring
- Explanation generation
- Code optimization

**Test the service**:
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

### watsonx Orchestrate Integration (Port 8004)

```bash
cd services/watsonx-orchestrate-integration
python -m app.handler
```

**Features**:
- Documentation generation
- Ticket creation
- Learning path generation

**Test the service**:
```bash
curl -X POST http://localhost:8004/api/v1/automate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def example(): pass",
    "language": "python",
    "analysis_results": {
      "debugging": {"bugs": []},
      "efficiency": {"time_complexity": {"current": "O(n)", "target": "O(n)"}}
    }
  }'
```

## Using the CLI Demo

The CLI demo provides an interactive interface to test the system.

### Start the CLI

```bash
cd demo/cli-demo
python app.py
```

### CLI Menu Options

```
Main Menu:

  1. Analyze Example Code (Buggy Python)
  2. Analyze Example Code (Inefficient Python)
  3. Analyze Custom Code
  4. View Example Files
  5. Check Service Health
  6. About This System
  0. Exit
```

### Example: Analyzing Buggy Code

1. Start the CLI: `python app.py`
2. Select option `1` (Analyze Example Code - Buggy Python)
3. View the comprehensive analysis results
4. Press Enter to return to the menu

### Example: Analyzing Custom Code

1. Start the CLI: `python app.py`
2. Select option `3` (Analyze Custom Code)
3. Choose language (1=Python, 2=C++, 3=Java)
4. Choose input method:
   - Option 1: Enter code directly (end with Ctrl+D/Ctrl+Z)
   - Option 2: Load from file (provide file path)
5. View analysis results

## Example Workflows

### Workflow 1: Complete Code Analysis

```python
# 1. Submit code for debugging analysis
import requests

code = """
def find_duplicates(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                duplicates.append(numbers[i])
    return duplicates
"""

# Debugging analysis
debug_response = requests.post(
    "http://localhost:8001/api/v1/analyze",
    json={"code": code, "language": "python"}
)
debug_results = debug_response.json()

# Efficiency analysis
efficiency_response = requests.post(
    "http://localhost:8002/api/v1/analyze",
    json={"code": code, "language": "python"}
)
efficiency_results = efficiency_response.json()

# Request refactoring
refactor_response = requests.post(
    "http://localhost:8003/api/v1/refactor",
    json={
        "code": code,
        "language": "python",
        "bugs": debug_results.get("bugs", []),
        "optimization_strategy": efficiency_results.get("recommended_strategy", "")
    }
)
refactored_code = refactor_response.json()

# Trigger automation
automation_response = requests.post(
    "http://localhost:8004/api/v1/automate",
    json={
        "code": code,
        "language": "python",
        "analysis_results": {
            "debugging": debug_results,
            "efficiency": efficiency_results
        }
    }
)
automation_results = automation_response.json()

print("Analysis complete!")
print(f"Bugs found: {len(debug_results.get('bugs', []))}")
print(f"Current complexity: {efficiency_results.get('time_complexity', {}).get('current')}")
print(f"Refactored code available: {bool(refactored_code.get('refactored_code'))}")
```

### Workflow 2: Batch Analysis

```python
import os
import requests

def analyze_directory(directory_path):
    """Analyze all Python files in a directory."""
    results = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.py'):
            filepath = os.path.join(directory_path, filename)
            
            with open(filepath, 'r') as f:
                code = f.read()
            
            # Analyze each file
            response = requests.post(
                "http://localhost:8001/api/v1/analyze",
                json={"code": code, "language": "python"}
            )
            
            results.append({
                "file": filename,
                "analysis": response.json()
            })
    
    return results

# Analyze all files in examples directory
results = analyze_directory("demo/cli-demo/examples")
for result in results:
    print(f"\n{result['file']}:")
    print(f"  Bugs: {len(result['analysis'].get('bugs', []))}")
```

### Workflow 3: Integration Testing

```bash
# Run all test suites
cd demo/test-cases

# Test debugging engine
python -m pytest test_debugging.py -v

# Test efficiency analyzer
python -m pytest test_efficiency.py -v

# Test end-to-end integration
python -m pytest test_integration.py -v

# Run all tests
python -m pytest -v
```

## Troubleshooting

### Common Issues

#### Issue: Services won't start

**Symptoms**: Error messages when starting services

**Solutions**:
1. Check if ports are already in use:
   ```bash
   # Windows
   netstat -ano | findstr :8001
   
   # Linux/Mac
   lsof -i :8001
   ```

2. Verify Python version:
   ```bash
   python --version  # Should be 3.11+
   ```

3. Reinstall dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

#### Issue: "Connection refused" errors

**Symptoms**: CLI or tests can't connect to services

**Solutions**:
1. Verify services are running:
   ```bash
   curl http://localhost:8001/health
   ```

2. Check firewall settings

3. Ensure correct ports in configuration

#### Issue: IBM watsonx authentication errors

**Symptoms**: 401 Unauthorized errors from watsonx services

**Solutions**:
1. Verify API key in `.env` file
2. Check API key permissions in IBM Cloud
3. Ensure project ID is correct
4. Verify watsonx URL is correct for your region

#### Issue: Import errors

**Symptoms**: `ModuleNotFoundError` when running services

**Solutions**:
1. Ensure you're in the correct directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check Python path:
   ```bash
   echo $PYTHONPATH
   ```

#### Issue: Docker containers won't start

**Symptoms**: Docker Compose errors

**Solutions**:
1. Check Docker is running:
   ```bash
   docker ps
   ```

2. Rebuild containers:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

3. Check logs:
   ```bash
   docker-compose logs service-name
   ```

### Getting Help

If you encounter issues not covered here:

1. Check the [API Reference](API_REFERENCE.md) for endpoint details
2. Review [Architecture Documentation](ARCHITECTURE.md) for system design
3. Check service-specific README files in `services/` directories
4. Review logs for error messages
5. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version, etc.)

## Next Steps

### Learn More

- **[API Reference](API_REFERENCE.md)**: Detailed API documentation
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)**: Production deployment instructions
- **[Architecture](ARCHITECTURE.md)**: System architecture details
- **[Project Summary](PROJECT_SUMMARY.md)**: High-level overview

### Explore Features

1. **Try Different Languages**: Test with Python, C++, and Java code
2. **Experiment with Examples**: Modify example files and re-analyze
3. **Create Custom Tests**: Add your own test cases
4. **Integrate with Tools**: Connect to your IDE or CI/CD pipeline

### Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Production Deployment

When ready for production:

1. Review [Deployment Guide](DEPLOYMENT_GUIDE.md)
2. Set up Kubernetes cluster
3. Configure monitoring and logging
4. Set up CI/CD pipelines
5. Configure backup and disaster recovery

## Quick Reference

### Service URLs (Default)

| Service | URL | Port |
|---------|-----|------|
| Debugging Engine | http://localhost:8001 | 8001 |
| Efficiency Analyzer | http://localhost:8002 | 8002 |
| watsonx.ai Integration | http://localhost:8003 | 8003 |
| watsonx Orchestrate | http://localhost:8004 | 8004 |

### Common Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Restart a service
docker-compose restart [service-name]

# Run CLI demo
cd demo/cli-demo && python app.py

# Run tests
cd demo/test-cases && python -m pytest -v

# Check service health
curl http://localhost:8001/health
```

### Environment Variables

```bash
# Required
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id

# Optional (with defaults)
DEBUGGING_ENGINE_PORT=8001
EFFICIENCY_ANALYZER_PORT=8002
WATSONX_AI_PORT=8003
WATSONX_ORCHESTRATE_PORT=8004
LOG_LEVEL=INFO
```

---

**Need Help?** Check the troubleshooting section or open an issue on GitHub.

**Ready for Production?** See the [Deployment Guide](DEPLOYMENT_GUIDE.md).
