# Algorithmic Debugging & Efficiency Coach

An intelligent code analysis system that diagnoses bugs and guides optimization from brute-force to production-ready solutions. Powered by IBM watsonx.ai and watsonx Orchestrate.

## 🎯 Overview

The Algorithmic Debugging & Efficiency Coach is a comprehensive microservices-based platform that helps developers:

- **Identify Bugs**: Detect syntax errors, logic errors, and runtime issues
- **Analyze Complexity**: Calculate time and space complexity with Big O notation
- **Optimize Code**: Get step-by-step optimization guides and refactored code
- **Automate Workflows**: Generate documentation, create tickets, and build learning paths

### Key Features

✨ **Multi-Language Support**: Python, C++, and Java  
🔍 **Deep Analysis**: Execution flow, root cause identification, and pattern detection  
🤖 **AI-Powered**: Leverages IBM watsonx.ai for intelligent code generation  
⚡ **Automated Workflows**: watsonx Orchestrate integration for documentation and ticketing  
📊 **Comprehensive Reports**: Detailed analysis with actionable recommendations  
🎨 **Interactive CLI**: User-friendly command-line interface for testing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                            │
│              (IBM API Connect + Cloud IAM)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
     ┌──────────▼──────────┐   ┌─────────▼──────────┐
     │  Core Services      │   │  Serverless Layer  │
     │  (Containerized)    │   │  (IBM Cloud Fns)   │
     └──────────┬──────────┘   └─────────┬──────────┘
                │                         │
    ┌───────────┼─────────────────────────┼───────────┐
    │           │                         │           │
┌───▼────┐ ┌───▼─────┐ ┌────────────────▼─────┐ ┌───▼────┐
│Debug   │ │Efficiency│ │watsonx Integration   │ │Output  │
│Engine  │ │Analyzer │ │Layer                 │ │Format  │
│:8001   │ │:8002    │ │:8003/:8004           │ │        │
└────────┘ └─────────┘ └──────────────────────┘ └────────┘
```

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| **Debugging Engine** | 8001 | Bug detection and execution flow analysis |
| **Efficiency Analyzer** | 8002 | Complexity calculation and optimization recommendations |
| **watsonx.ai Integration** | 8003 | Code refactoring and generation using IBM watsonx.ai |
| **watsonx Orchestrate** | 8004 | Workflow automation for documentation and ticketing |

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker & Docker Compose (optional)
- IBM Cloud account with watsonx access

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd algo-coach

# Set up environment variables
cp .env.example .env
# Edit .env with your IBM watsonx credentials

# Option 1: Using Docker Compose (Recommended)
docker-compose up -d

# Option 2: Run services individually
cd services/debugging-engine && python -m app.main &
cd services/efficiency-analyzer && python -m app.main &
cd services/watsonx-ai-integration && python -m app.handler &
cd services/watsonx-orchestrate-integration && python -m app.handler &
```

### Verify Installation

```bash
# Check all services are running
curl http://localhost:8001/health  # Debugging Engine
curl http://localhost:8002/health  # Efficiency Analyzer
curl http://localhost:8003/health  # watsonx.ai Integration
curl http://localhost:8004/health  # watsonx Orchestrate
```

### Try the CLI Demo

```bash
cd demo/cli-demo
pip install -r requirements.txt
python app.py
```

## 📖 Documentation

Comprehensive documentation is available:

- **[Getting Started Guide](GETTING_STARTED.md)** - Installation and setup instructions
- **[API Reference](API_REFERENCE.md)** - Complete API documentation for all services
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[Architecture](ARCHITECTURE.md)** - Detailed system architecture and design
- **[Project Summary](PROJECT_SUMMARY.md)** - High-level overview and features

## 💡 Usage Examples

### Example 1: Analyze Buggy Code

```python
import requests

code = """
def find_max(numbers):
    max_val = numbers[0]
    for i in range(1, len(numbers) + 1):  # Bug: off-by-one error
        if numbers[i] > max_val:
            max_val = numbers[i]
    return max_val
"""

response = requests.post(
    "http://localhost:8001/api/v1/analyze",
    json={"code": code, "language": "python"}
)

results = response.json()
print(f"Bugs found: {len(results['data']['bugs'])}")
print(f"Explanation: {results['data']['explanation']}")
```

### Example 2: Analyze Inefficient Code

```python
code = """
def find_pair(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None
"""

response = requests.post(
    "http://localhost:8002/api/v1/analyze",
    json={"code": code, "language": "python"}
)

results = response.json()
print(f"Current complexity: {results['data']['time_complexity']['current']}")
print(f"Target complexity: {results['data']['time_complexity']['target']}")
print(f"Strategy: {results['data']['recommended_strategy']}")
```

### Example 3: Get Refactored Code

```python
response = requests.post(
    "http://localhost:8003/api/v1/refactor",
    json={
        "code": code,
        "language": "python",
        "bugs": [],
        "optimization_strategy": "Use hash map"
    }
)

results = response.json()
print("Refactored code:")
print(results['data']['refactored_code'])
```

## 🎨 CLI Demo Features

The interactive CLI provides:

- **Pre-loaded Examples**: Buggy and inefficient code samples
- **Custom Code Analysis**: Analyze your own code
- **Service Health Monitoring**: Check all microservices status
- **Colored Output**: Clear, formatted results
- **Multiple Languages**: Support for Python, C++, and Java

### CLI Menu

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

## 🧪 Testing

### Run Test Suites

```bash
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

### Sample Test Cases

The project includes comprehensive test cases:

- **Python**: `nested_loops.py`, `recursive_fib.py`, `syntax_error.py`
- **C++**: `memory_leak.cpp`
- **Java**: `inefficient_sort.java`

## 🛠️ Technology Stack

### Backend Services
- **Python 3.11+** with FastAPI
- **AST Parsing** for code analysis
- **Async/Await** for performance

### AI & Automation
- **IBM watsonx.ai** - Code generation and refactoring
- **IBM watsonx Orchestrate** - Workflow automation

### Infrastructure
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **PostgreSQL** - Data persistence
- **Redis** - Caching

## 📊 Output Format

Analysis results follow a consistent structure:

```
=== DIAGNOSTIC SUMMARY ===
[Bug descriptions and explanations]

=== COMPLEXITY BREAKDOWN ===
Current Time Complexity: O(n²)
Current Space Complexity: O(n)
Target Time Complexity: O(n)
Target Space Complexity: O(n)

=== THE OPTIMIZATION PATH ===
Step 1: Use Hash Map for O(1) lookups
Step 2: Single pass solution
...

=== AUTOMATED ACTIONS ===
✓ Documentation updated: docs/analysis_report.md
✓ Tickets created: TECH-1234, TECH-1235
✓ Learning path generated: Hash Maps, Algorithm Optimization
```

## 🔒 Security

- **Authentication**: IBM Cloud IAM for production
- **Encryption**: TLS 1.3 for data in transit
- **Data Protection**: AES-256 for data at rest
- **Network Security**: VPC isolation and security groups

## 📈 Performance

- **Response Time**: < 2s (p95)
- **Throughput**: 100 requests/second
- **Availability**: 99.9% uptime SLA
- **Auto-scaling**: HPA based on CPU/memory

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python
- Write unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📝 Project Structure

```
algo-coach/
├── services/                    # Core microservices
│   ├── debugging-engine/       # Bug detection service
│   ├── efficiency-analyzer/    # Complexity analysis service
│   ├── watsonx-ai-integration/ # watsonx.ai integration
│   └── watsonx-orchestrate-integration/
├── demo/                        # Demo applications
│   ├── cli-demo/               # Interactive CLI
│   └── test-cases/             # Test suites
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── GETTING_STARTED.md
├── docker-compose.yml          # Docker Compose configuration
├── README.md                   # This file
└── LICENSE                     # License information
```

## 🎯 Use Cases

### For Developers
- Debug complex code issues
- Optimize algorithm performance
- Learn best practices
- Prepare for technical interviews

### For Students
- Understand algorithmic complexity
- Learn optimization techniques
- Practice coding problems
- Get instant feedback

### For Educators
- Teach algorithm design
- Demonstrate optimization
- Provide automated feedback
- Track student progress

### For Teams
- Code review automation
- Performance optimization
- Knowledge sharing
- Technical debt reduction

## 🌟 Roadmap

### Phase 1 (Current)
- ✅ Core debugging engine
- ✅ Efficiency analyzer
- ✅ watsonx.ai integration
- ✅ watsonx Orchestrate integration
- ✅ CLI demo application

### Phase 2 (Planned)
- [ ] Support for additional languages (Go, Rust, TypeScript)
- [ ] Web-based UI
- [ ] IDE plugins (VS Code, IntelliJ)
- [ ] Real-time collaboration
- [ ] Advanced visualization

### Phase 3 (Future)
- [ ] Mobile application
- [ ] Custom model fine-tuning
- [ ] Automated test generation
- [ ] CI/CD pipeline integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IBM watsonx** for AI capabilities
- **FastAPI** for the excellent web framework
- **Docker** for containerization
- **Kubernetes** for orchestration
- All contributors and users

## 📞 Support

- **Documentation**: See `/docs` directory
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: support@example.com

## 🔗 Links

- [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai)
- [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

**Built with ❤️ using IBM watsonx**

**Version**: 1.0.0  
**Last Updated**: 2026-05-02  
**Status**: Production Ready



---




# Algorithmic Debugging & Efficiency Coach - System Architecture

## Executive Summary

This document outlines the architecture for an intelligent code analysis system that diagnoses bugs and guides optimization from brute-force to production-ready solutions. The system supports C++, Python, and Java, leveraging IBM watsonx.ai for intelligent code generation and watsonx Orchestrate for workflow automation.

**Deployment Model:** Hybrid approach with containerized core services and serverless watsonx integrations  
**Database:** Hybrid - PostgreSQL (structured data) + Redis (caching) + S3 (code storage)  
**API Gateway:** IBM API Connect with IBM Cloud IAM authentication  
**Target Users:** Developers, students, coding interview candidates, technical educators

---

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          API Gateway Layer                               │
│                    (IBM API Connect + Cloud IAM)                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
         ┌──────────▼──────────┐   ┌─────────▼──────────┐
         │  Core Services      │   │  Serverless Layer  │
         │  (Containerized)    │   │  (IBM Cloud Fns)   │
         └──────────┬──────────┘   └─────────┬──────────┘
                    │                         │
    ┌───────────────┼─────────────────────────┼───────────────┐
    │               │                         │               │
┌───▼────┐   ┌─────▼──────┐   ┌──────────────▼─────┐   ┌────▼─────┐
│Debugging│   │ Efficiency │   │ watsonx Integration│   │  Output  │
│ Engine  │   │  Analyzer  │   │      Layer         │   │Formatter │
└───┬────┘   └─────┬──────┘   └──────────┬─────────┘   └────┬─────┘
    │              │                      │                   │
    └──────────────┴──────────────────────┴───────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Data Layer           │
                    │ PostgreSQL + Redis + S3 │
                    └─────────────────────────┘
```

### Architecture Layers

1. **API Gateway Layer**: Entry point for all requests, handles authentication, rate limiting, and routing
2. **Core Services Layer**: Containerized microservices for debugging and efficiency analysis
3. **Serverless Layer**: IBM Cloud Functions for watsonx integrations and workflow automation
4. **Data Layer**: Hybrid storage solution for different data types
5. **Integration Layer**: Connects to external IBM watsonx services

---

## 2. Core Components Design

### 2.1 Debugging Engine (Phase 1)

**Purpose:** Analyze code execution, identify bugs, and provide plain-language explanations

**Sub-components:**

#### 2.1.1 Execution Flow Analyzer
- **Technology:** Tree-sitter (multi-language parsing) + Custom AST walker
- **Functionality:**
  - Parse source code into Abstract Syntax Tree (AST)
  - Map execution paths and control flow
  - Identify unreachable code and dead branches
  - Track variable scope and lifecycle

#### 2.1.2 Root Cause Identifier
- **Technology:** Static analysis engines per language
  - C++: Clang Static Analyzer
  - Python: Pylint + Mypy
  - Java: SpotBugs + Error Prone
- **Functionality:**
  - Syntax error detection with precise location
  - Logic error identification (infinite loops, null pointers, type mismatches)
  - Memory error detection (leaks, buffer overflows, dangling pointers)
  - Runtime error prediction

#### 2.1.3 Plain-Language Bug Explainer
- **Technology:** watsonx.ai (granite-13b-chat-v2 model)
- **Functionality:**
  - Convert technical error messages to beginner-friendly explanations
  - Provide context-aware suggestions
  - Generate fix recommendations with code examples

**Container Specification:**
```yaml
Service: debugging-engine
Base Image: python:3.11-slim
Dependencies: tree-sitter, clang-tools, pylint, mypy, spotbugs
Ports: 8001
Resources: 2 CPU, 4GB RAM
```

---

### 2.2 Efficiency Analyzer (Phase 2)

**Purpose:** Calculate complexity, detect inefficient patterns, and recommend optimizations

**Sub-components:**

#### 2.2.1 Time/Space Complexity Calculator
- **Technology:** Custom complexity analysis engine + SymPy for mathematical analysis
- **Functionality:**
  - Analyze loop structures and nesting depth
  - Identify recursive patterns and calculate recurrence relations
  - Detect data structure operations and their complexities
  - Generate Big O notation for time and space

#### 2.2.2 Brute-Force Pattern Detector
- **Technology:** Pattern matching with regex + AST analysis
- **Patterns Detected:**
  - Nested loops (O(n²), O(n³))
  - Redundant recursion without memoization
  - Linear search in sorted data
  - Suboptimal data structures (arrays vs hash maps)
  - Repeated computations
  - Unnecessary string concatenations

#### 2.2.3 Optimization Strategy Recommender
- **Technology:** Rule-based engine + watsonx.ai for intelligent suggestions

- **Strategies Recommended:**
  - Sliding Window (for subarray/substring problems)
  - Two Pointers (for sorted array problems)
  - Dynamic Programming (for overlapping subproblems)
  - Hash Maps (for O(1) lookups)
  - Greedy Algorithms (for optimization problems)
  - Graph Algorithms (BFS, DFS, Dijkstra)

**Container Specification:**
```yaml
Service: efficiency-analyzer
Base Image: python:3.11-slim
Dependencies: sympy, networkx, tree-sitter
Ports: 8002
Resources: 2 CPU, 4GB RAM
```

---

### 2.3 watsonx Integration Layer

**Purpose:** Leverage IBM watsonx.ai and watsonx Orchestrate for intelligent code operations

#### 2.3.1 watsonx.ai Integration (Serverless)
- **Model:** IBM granite-20b-code-instruct
- **Use Cases:**
  - Code refactoring and optimization
  - Bug fix generation
  - Code explanation and documentation
  - Alternative implementation suggestions

**Function Specification:**
```yaml
Function: watsonx-ai-service
Runtime: Python 3.11
Memory: 2GB
Timeout: 60s
Trigger: HTTP + Event-driven
Environment:
  WATSONX_API_KEY: ${SECRET}
  MODEL_ID: ibm/granite-20b-code-instruct
```

#### 2.3.2 watsonx Orchestrate Integration (Serverless)
- **Workflows:**
  - Documentation generation (README, API docs)
  - Ticket creation (Jira, GitHub Issues)
  - Learning path generation
  - Code review automation

**Function Specification:**
```yaml
Function: watsonx-orchestrate-service
Runtime: Node.js 18
Memory: 1GB
Timeout: 120s
Trigger: Event-driven
Environment:
  ORCHESTRATE_API_KEY: ${SECRET}
  JIRA_API_KEY: ${SECRET}
```

---

### 2.4 Output Formatter

**Purpose:** Consolidate analysis results into structured, user-friendly reports

**Functionality:**
- Aggregate results from debugging and efficiency analyzers
- Format output in multiple formats (JSON, HTML, PDF, Markdown)
- Generate visual diagrams (complexity graphs, execution flow)
- Prepare data for watsonx integrations

**Container Specification:**
```yaml
Service: output-formatter
Base Image: node:18-alpine
Dependencies: express, handlebars, puppeteer
Ports: 8003
Resources: 1 CPU, 2GB RAM
```

---

## 3. Technology Stack

### 3.1 Core Services (Containerized)

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Debugging Engine** | Python + FastAPI | 3.11 | Rich parsing libraries, excellent static analysis ecosystem |
| **Efficiency Analyzer** | Python + FastAPI | 3.11 | Scientific computing libraries (SymPy, NetworkX) |
| **Output Formatter** | Node.js + Express | 18 LTS | Fast JSON processing, template engines |
| **Container Runtime** | Docker | 24.x | Industry standard, IBM Cloud support |
| **Orchestration** | Kubernetes (IKS) | 1.28+ | Auto-scaling, self-healing, IBM native |

### 3.2 Serverless Functions

| Function | Runtime | Platform | Rationale |
|----------|---------|----------|-----------|
| **watsonx.ai Integration** | Python 3.11 | IBM Cloud Functions | Native IBM SDK, async capabilities |
| **watsonx Orchestrate** | Node.js 18 | IBM Cloud Functions | Event-driven, webhook handling |

### 3.3 Data Layer

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Primary Database** | PostgreSQL | 15.x | ACID compliance, JSON support, mature |
| **Cache Layer** | Redis | 7.x | Sub-millisecond latency, pub/sub |
| **Object Storage** | IBM Cloud Object Storage | N/A | Cost-effective, S3-compatible |
| **Message Queue** | Redis (Bull) | 7.x | Simple setup, persistent queues |

### 3.4 API & Integration

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **API Gateway** | IBM API Connect | Enterprise features, IAM integration |
| **Authentication** | IBM Cloud IAM | Centralized identity, OAuth 2.0 |
| **Service Mesh** | Istio | Traffic management, observability |

### 3.5 Language-Specific Tools

| Language | Parser | Linter | Static Analyzer |
|----------|--------|--------|-----------------|
| **C++** | Clang/LLVM | clang-tidy | Clang Static Analyzer, cppcheck |
| **Python** | ast (built-in) | pylint, flake8 | mypy, bandit |
| **Java** | JavaParser | Checkstyle | SpotBugs, PMD |
| **Universal** | Tree-sitter | N/A | Custom rules engine |

---

## 4. Data Architecture

### 4.1 PostgreSQL Schema Design

#### Core Tables

**users**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subscription_tier VARCHAR(50) DEFAULT 'free',
    preferences JSONB DEFAULT '{}',
    INDEX idx_email (email)
);
```

**submissions**
```sql
CREATE TABLE submissions (
    submission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    language VARCHAR(20) NOT NULL CHECK (language IN ('cpp', 'python', 'java')),
    code_hash VARCHAR(64) UNIQUE NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    INDEX idx_user_submissions (user_id, submitted_at DESC),
    INDEX idx_code_hash (code_hash)
);
```

**analysis_results**
```sql
CREATE TABLE analysis_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(submission_id) ON DELETE CASCADE,
    analysis_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    completed_at TIMESTAMP,
    execution_time_ms INTEGER,
    result_data JSONB NOT NULL,
    INDEX idx_submission (submission_id)
);
```

**bugs**
```sql
CREATE TABLE bugs (
    bug_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES analysis_results(result_id) ON DELETE CASCADE,
    bug_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    line_number INTEGER NOT NULL,
    message TEXT NOT NULL,
    explanation TEXT,
    fix_suggestion TEXT,
    INDEX idx_severity (severity)
);
```

**complexity_analysis**
```sql
CREATE TABLE complexity_analysis (
    complexity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES analysis_results(result_id) ON DELETE CASCADE,
    current_time_complexity VARCHAR(50) NOT NULL,
    current_space_complexity VARCHAR(50) NOT NULL,
    target_time_complexity VARCHAR(50),
    target_space_complexity VARCHAR(50),
    improvement_potential DECIMAL(5,2),
    detected_patterns JSONB
);
```

**optimization_recommendations**
```sql
CREATE TABLE optimization_recommendations (
    recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complexity_id UUID REFERENCES complexity_analysis(complexity_id) ON DELETE CASCADE,
    strategy VARCHAR(100) NOT NULL,
    priority INTEGER DEFAULT 1,
    description TEXT NOT NULL,
    steps JSONB NOT NULL,
    code_example TEXT,
    estimated_improvement VARCHAR(100)
);
```

**watsonx_jobs**
```sql
CREATE TABLE watsonx_jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(submission_id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL,
    service VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    output_data JSONB,
    INDEX idx_status (status)
);
```

### 4.2 Redis Caching Strategy

**Cache Key Patterns:**
```
submission:{code_hash} → Full analysis results (TTL: 7 days)
user:{user_id}:recent → Recent submission IDs (TTL: 1 day)
analysis:{submission_id} → Analysis status (TTL: 1 hour)
rate_limit:{user_id}:{endpoint} → Rate limiting (TTL: 1 minute)
```

**Cache Layers:**
- **L1 (Hot)**: Active analyses, session data (5 min TTL, 100MB)
- **L2 (Warm)**: Recent results, user activity (7 days TTL, 5GB)
- **L3 (Cold)**: PostgreSQL + S3 (permanent storage)

### 4.3 S3 Bucket Structure

```
code-submissions-bucket/
├── submissions/
│   └── {year}/{month}/{day}/{submission_id}.{ext}
├── analysis-results/
│   └── {submission_id}/
│       ├── debugging-report.json
│       └── efficiency-report.json
├── refactored-code/
│   └── {submission_id}/
│       ├── original.{ext}
│       └── optimized.{ext}
└── documentation/
    └── {submission_id}/
        └── README.md
```

**Lifecycle Policy:**
- Archive to Glacier after 90 days
- Delete temp files after 30 days
- Enable versioning for code submissions

---

## 5. API Specifications

### 5.1 Base Configuration

**Base URL:** `https://api.algo-coach.ibm.cloud`

**Authentication:** IBM Cloud IAM Bearer Token
```
Authorization: Bearer {IAM_TOKEN}
```

**Rate Limits:**
- Free: 10 requests/hour
- Pro: 100 requests/hour
- Enterprise: Unlimited

### 5.2 Core Endpoints

#### Submit Code for Analysis
```
POST /api/v1/submissions
Content-Type: application/json

Request:
{
  "language": "python|cpp|java",
  "code": "base64_encoded_code",
  "filename": "solution.py",
  "analysis_types": ["debugging", "efficiency"],
  "options": {
    "enable_watsonx_refactoring": true,
    "target_complexity": "O(n)"
  }
}

Response (202 Accepted):
{
  "submission_id": "uuid",
  "status": "pending",
  "estimated_completion_time": "ISO-8601",
  "status_url": "/api/v1/submissions/{id}/status"
}
```

#### Get Submission Status
```
GET /api/v1/submissions/{submission_id}/status

Response:
{
  "submission_id": "uuid",
  "status": "processing|completed|failed",
  "progress": {
    "debugging": {"status": "completed", "progress_percent": 100},
    "efficiency": {"status": "processing", "progress_percent": 65}
  }
}
```

#### Get Analysis Results
```
GET /api/v1/submissions/{submission_id}/results
Query: ?format=json|html|pdf

Response:
{
  "submission_id": "uuid",
  "diagnostic_summary": {
    "status": "warning",
    "bug_count": 2,
    "bugs": [...]
  },
  "complexity_breakdown": {
    "current": {"time": "O(n^2)", "space": "O(1)"},
    "target": {"time": "O(n)", "space": "O(n)"}
  },
  "optimization_path": {
    "recommended_strategy": "Hash Map",
    "steps": [...]
  },
  "watsonx_actions": {...}
}
```

#### Get Refactored Code
```
GET /api/v1/watsonx/jobs/{job_id}/result

Response:
{
  "job_id": "uuid",
  "status": "completed",
  "result": {
    "original_code": "...",
    "refactored_code": "...",
    "explanation": "..."
  }
}
```

### 5.3 WebSocket API

**Real-time Progress Updates:**
```
wss://api.algo-coach.ibm.cloud/ws/{submission_id}

Messages:
{
  "type": "progress",
  "stage": "debugging|efficiency|watsonx",
  "progress_percent": 75,
  "message": "Analyzing complexity..."
}
```

---

## 6. Integration Layer Design

### 6.1 watsonx.ai Integration

**API Client Implementation:**
```python
from ibm_watsonx_ai import APIClient, Credentials

class WatsonxAIService:
    def __init__(self):
        self.credentials = Credentials(
            url="https://us-south.ml.cloud.ibm.com",
            api_key=os.getenv("WATSONX_API_KEY")
        )
        self.client = APIClient(self.credentials)
        self.model_id = "ibm/granite-20b-code-instruct"
    
    async def refactor_code(self, code: str, language: str, goal: str):
        prompt = self._build_refactoring_prompt(code, language, goal)
        
        params = {
            "decoding_method": "greedy",
            "max_new_tokens": 2048,
            "temperature": 0.2,
            "repetition_penalty": 1.1
        }
        
        response = await self.client.foundation_models.generate_async(
            model_id=self.model_id,
            prompt=prompt,
            params=params,
            project_id=os.getenv("WATSONX_PROJECT_ID")
        )
        
        return self._parse_response(response)
```

**Prompt Templates:**
```python
REFACTORING_PROMPT = """
You are an expert code optimizer. Analyze and optimize this {language} code.

Original Code:
```{language}
{code}
```

Current Complexity: {current_complexity}
Target Complexity: {target_complexity}

Provide:
1. Optimized code
2. Explanation of improvements
3. Complexity analysis

Format as JSON.
"""
```

### 6.2 watsonx Orchestrate Integration

**Workflow Definitions:**
```javascript
const WORKFLOWS = {
  documentation_generation: {
    name: "Generate Documentation",
    steps: [
      {action: "analyze_code_structure", input: "submission_id"},
      {action: "generate_readme", model: "granite-code"},
      {action: "store_documentation", destination: "s3"}
    ]
  },
  ticket_creation: {
    name: "Create Bug Tickets",
    steps: [
      {action: "extract_bugs", input: "analysis_results"},
      {action: "prioritize_bugs", criteria: "severity"},
      {action: "create_jira_tickets", project: "DEV"}
    ]
  }
};
```

**API Client:**
```javascript
class OrchestratClient {
  async executeWorkflow(workflowName, input) {
    const response = await axios.post(
      `${this.baseUrl}/v1/workflows/execute`,
      {
        workflow_definition: WORKFLOWS[workflowName],
        input_data: input,
        async: true
      },
      {headers: {'Authorization': `Bearer ${this.apiKey}`}}
    );
    return response.data;
  }
}
```

---

## 7. Deployment Architecture

### 7.1 Container Deployment (Kubernetes)

**Namespace Structure:**
```yaml
Namespaces:
  - algo-coach-prod
  - algo-coach-staging
  - algo-coach-dev
```

**Service Deployments:**
```yaml
# Debugging Engine Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debugging-engine
  namespace: algo-coach-prod
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
        image: icr.io/algo-coach/debugging-engine:latest
        ports:
        - containerPort: 8001
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        env:
        - name: POSTGRES_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8001
          initialDelaySeconds: 10
          periodSeconds: 5
---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: debugging-engine-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: debugging-engine
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 7.2 Serverless Deployment

**IBM Cloud Functions Configuration:**
```yaml
# watsonx.ai Integration Function
functions:
  watsonx-ai-service:
    runtime: python:3.11
    memory: 2048
    timeout: 60000
    environment:
      WATSONX_API_KEY: ${SECRET}
      MODEL_ID: ibm/granite-20b-code-instruct
    triggers:
      - http:
          method: POST
          path: /watsonx/refactor
      - event:
          type: analysis.completed
```

### 7.3 Infrastructure as Code (Terraform)

**Main Configuration:**
```hcl
# IBM Cloud Kubernetes Service
resource "ibm_container_cluster" "algo_coach_cluster" {
  name              = "algo-coach-cluster"
  datacenter        = "dal10"
  machine_type      = "bx2.4x16"
  hardware          = "shared"
  public_vlan_id    = var.public_vlan_id
  private_vlan_id   = var.private_vlan_id
  default_pool_size = 3
  
  kube_version = "1.28"
}

# PostgreSQL Database
resource "ibm_database" "postgresql" {
  name              = "algo-coach-db"
  plan              = "standard"
  location          = "us-south"
  service           = "databases-for-postgresql"
  version           = "15"
  
  group {
    group_id = "member"
    memory {
      allocation_mb = 8192
    }
    disk {
      allocation_mb = 102400
    }
    cpu {
      allocation_count = 4
    }
  }
}

# Redis Cache
resource "ibm_database" "redis" {
  name     = "algo-coach-cache"
  plan     = "standard"
  location = "us-south"
  service  = "databases-for-redis"
  version  = "7.0"
  
  group {
    group_id = "member"
    memory {
      allocation_mb = 4096
    }
  }
}

# Object Storage
resource "ibm_cos_bucket" "code_submissions" {
  bucket_name          = "algo-coach-submissions"
  resource_instance_id = ibm_resource_instance.cos.id
  region_location      = "us-south"
  storage_class        = "smart"
}
```

---

## 8. Security Architecture

### 8.1 Authentication & Authorization

**IBM Cloud IAM Integration:**
```
User Request
    │
    ▼
[API Gateway]
    │
    ▼
Validate IAM Token
    │
    ├─ Valid ──► Extract user_id & permissions
    │                │
    │                ▼
    │           Check RBAC policies
    │                │
    │                ▼
    │           Route to service
    │
    └─ Invalid ──► Return 401 Unauthorized
```

**Role-Based Access Control (RBAC):**
```yaml
Roles:
  - free_user:
      permissions:
        - submit_code
        - view_own_results
      limits:
        - max_submissions_per_hour: 10
        - max_code_size: 10KB
  
  - pro_user:
      permissions:
        - submit_code
        - view_own_results
        - enable_watsonx_features
      limits:
        - max_submissions_per_hour: 100
        - max_code_size: 50KB
  
  - enterprise_user:
      permissions:
        - submit_code
        - view_own_results
        - enable_watsonx_features
        - batch_submissions
        - api_access
      limits:
        - max_submissions_per_hour: unlimited
        - max_code_size: 500KB
```

### 8.2 Data Security

**Encryption:**
- **In Transit**: TLS 1.3 for all API communications
- **At Rest**: AES-256 encryption for S3 and database
- **Secrets Management**: IBM Secrets Manager for API keys

**Code Sanitization:**
```python
def sanitize_code(code: str, language: str) -> str:
    """
    Remove potentially malicious code patterns
    """
    # Remove system calls
    dangerous_patterns = [
        r'os\.system',
        r'subprocess\.',
        r'eval\(',
        r'exec\(',
        r'__import__',
        r'open\(',  # File operations
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            raise SecurityError(f"Dangerous pattern detected: {pattern}")
    
    return code
```

### 8.3 Network Security

**Service Mesh (Istio) Configuration:**
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: algo-coach-prod
spec:
  mtls:
    mode: STRICT

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: debugging-engine-policy
spec:
  selector:
    matchLabels:
      app: debugging-engine
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/algo-coach-prod/sa/api-gateway"]
    to:
    - operation:
        methods: ["POST", "GET"]
```

---

## 9. Data Flow Diagrams

### 9.1 Code Submission Flow

```
User
  │
  │ 1. POST /api/v1/submissions
  ▼
[API Gateway]
  │
  │ 2. Authenticate & validate
  ▼
[Code Ingestion Service]
  │
  ├─ 3a. Calculate code_hash
  │      │
  │      ▼
  │   [Redis Cache]
  │      │
  │      ├─ Cache Hit ──► Return cached results
  │      │
  │      └─ Cache Miss ──► Continue
  │
  ├─ 3b. Store code in S3
  │      │
  │      ▼
  │   [S3 Bucket]
  │
  ├─ 3c. Create submission record
  │      │
  │      ▼
  │   [PostgreSQL]
  │
  └─ 4. Queue analysis jobs
         │
         ▼
      [Redis Queue]
         │
         ├──► [Debugging Engine]
         │         │
         │         ▼
         │    Analyze bugs
         │         │
         │         ▼
         │    Store results
         │
         └──► [Efficiency Analyzer]
                   │
                   ▼
              Calculate complexity
                   │
                   ▼
              Detect patterns
                   │
                   ▼
              Store results
         │
         ▼
[Output Formatter]
         │
         ├──► Format response
         │
         └──► Trigger watsonx jobs (async)
                   │
                   ▼
              [watsonx Services]
         │
         ▼
Return results to user
```

### 9.2 watsonx Integration Flow

```
Analysis Complete
      │
      ▼
[Output Formatter]
      │
      ├─ Check if watsonx enabled
      │
      ▼
Create watsonx jobs
      │
      ├──► [watsonx.ai Function]
      │         │
      │         ├─ 1. Refactor code
      │         │      │
      │         │      ▼
      │         │   Call granite-code model
      │         │      │
      │         │      ▼
      │         │   Generate optimized code
      │         │      │
      │         │      ▼
      │         │   Store in S3
      │         │
      │         └─ 2. Generate explanations
      │
      └──► [watsonx Orchestrate Function]
                │
                ├─ 1. Generate documentation
                │      │
                │      ▼
                │   Create README
                │      │
                │      ▼
                │   Store in S3
                │
                ├─ 2. Create tickets
                │      │
                │      ▼
                │   Call Jira API
                │      │
                │      ▼
                │   Link to submission
                │
                └─ 3. Generate learning path
                       │
                       ▼
                   Analyze knowledge gaps
                       │
                       ▼
                   Recommend resources
      │
      ▼
Update job status
      │
      ▼
Notify user (webhook/email)
```

---

## 10. Sequence Diagrams

### 10.1 Debugging Workflow

```
User          API Gateway    Ingestion    Debugging    PostgreSQL    watsonx.ai
 │                │              │           Engine         │             │
 │ Submit Code    │              │             │            │             │
 ├───────────────>│              │             │            │             │
 │                │ Authenticate │             │            │             │
 │                ├─────────────>│             │            │             │
 │                │              │ Store Code  │            │             │
 │                │              ├────────────>│            │             │
 │                │              │             │ Save Meta  │             │
 │                │              │             ├───────────>│             │
 │                │              │             │            │             │
 │                │              │ Parse AST   │            │             │
 │                │              │<────────────┤            │             │
 │                │              │             │            │             │
 │                │              │ Analyze Bugs│            │             │
 │                │              │<────────────┤            │             │
 │                │              │             │            │             │
 │                │              │             │ Save Results│            │
 │                │              │             ├───────────>│             │
 │                │              │             │            │             │
 │                │              │ Generate Fix│            │             │
 │                │              │ Suggestions │            │             │
 │                │              │─────────────────────────────────────>│
 │                │              │             │            │  Refactor  │
 │                │              │<─────────────────────────────────────┤
 │                │              │             │            │             │
 │ Return Results │              │             │            │             │
 │<───────────────┤              │             │            │             │
```

### 10.2 Efficiency Analysis Workflow

```
Ingestion    Efficiency    Complexity    Pattern      Recommender    PostgreSQL
Service      Analyzer      Calculator    Detector                         │
   │             │             │             │              │              │
   │ Analyze     │             │             │              │              │
   ├────────────>│             │             │              │              │
   │             │ Calculate   │             │              │              │
   │             ├────────────>│             │              │              │
   │             │             │ Build CFG   │              │              │
   │             │             ├─────────────┤              │              │
   │             │             │             │              │              │
   │             │             │ Analyze     │              │              │
   │             │             │ Loops       │              │              │
   │             │             ├─────────────┤              │              │
   │             │             │             │              │              │
   │             │<────────────┤ O(n^2)      │              │              │
   │             │             │             │              │              │
   │             │ Detect      │             │              │              │
   │             │ Patterns    │             │              │              │
   │             ├─────────────────────────>│              │              │
   │             │             │             │ Nested Loops │              │
   │             │<─────────────────────────┤              │              │
   │             │             │             │              │              │
   │             │ Recommend   │             │              │              │
   │             │ Strategy    │             │              │              │
   │             ├──────────────────────────────────────>│              │
   │             │             │             │              │ Hash Map    │
   │             │<──────────────────────────────────────┤              │
   │             │             │             │              │              │
   │             │ Save        │             │              │              │
   │             │ Results     │             │              │              │
   │             ├─────────────────────────────────────────────────────>│
   │<────────────┤             │             │              │              │
```

---

## 11. File/Directory Structure

```
algo-coach/
├── services/
│   ├── code-ingestion/
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   │   └── submission.controller.ts
│   │   │   ├── services/
│   │   │   │   ├── validation.service.ts
│   │   │   │   ├── storage.service.ts
│   │   │   │   └── queue.service.ts
│   │   │   ├── models/
│   │   │   │   └── submission.model.ts
│   │   │   ├── utils/
│   │   │   │   ├── hash.util.ts
│   │   │   │   └── parser.util.ts
│   │   │   └── app.ts
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── debugging-engine/
│   │   ├── src/
│   │   │   ├── analyzers/
│   │   │   │   ├── flow_analyzer.py
│   │   │   │   ├── root_cause_identifier.py
│   │   │   │   └── bug_explainer.py
│   │   │   ├── parsers/
│   │   │   │   ├── cpp_parser.py
│   │   │   │   ├── python_parser.py
│   │   │   │   └── java_parser.py
│   │   │   ├── models/
│   │   │   │   └── bug.py
│   │   │   ├── utils/
│   │   │   │   └── ast_utils.py
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── pyproject.toml
│   │
│   ├── efficiency-analyzer/
│   │   ├── src/
│   │   │   ├── analyzers/
│   │   │   │   ├── complexity_calculator.py
│   │   │   │   ├── pattern_detector.py
│   │   │   │   └── strategy_recommender.py
│   │   │   ├── models/
│   │   │   │   ├── complexity.py
│   │   │   │   └── optimization.py
│   │   │   ├── rules/
│   │   │   │   ├── pattern_rules.yaml
│   │   │   │   └── strategy_rules.yaml
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── output-formatter/
│       ├── src/
│       │   ├── formatters/
│       │   │   ├── json.formatter.ts
│       │   │   ├── html.formatter.ts
│       │   │   └── pdf.formatter.ts
│       │   ├── templates/
│       │   │   ├── report.hbs
│       │   │   └── summary.hbs
│       │   └── app.ts
│       ├── tests/
│       ├── Dockerfile
│       └── package.json
│
├── functions/
│   ├── watsonx-ai/
│   │   ├── src/
│   │   │   ├── handlers/
│   │   │   │   ├── refactor.py
│   │   │   │   ├── explain.py
│   │   │   │   └── fix.py
│   │   │   ├── clients/
│   │   │   │   └── watsonx_client.py
│   │   │   ├── prompts/
│   │   │   │   └── templates.py
│   │   │   └── main.py
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   └── watsonx-orchestrate/
│       ├── src/
│       │   ├── workflows/
│       │   │   ├── documentation.js
│       │   │   ├── tickets.js
│       │   │   └── learning.js
│       │   ├── clients/
│       │   │   ├── orchestrate.client.js
│       │   │   └── jira.client.js
│       │   └── index.js
│       ├── tests/
│       └── package.json
│
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── modules/
│   │   │   ├── kubernetes/
│   │   │   ├── database/
│   │   │   ├── storage/
│   │   │   └── functions/
│   │   └── environments/
│   │       ├── prod/
│   │       ├── staging/
│   │       └── dev/
│   │
│   └── kubernetes/
│       ├── base/
│       │   ├── deployments/
│       │   ├── services/
│       │   ├── configmaps/
│       │   └── secrets/
│       └── overlays/
│           ├── prod/
│           ├── staging/
│           └── dev/
│
├── database/
│   ├── migrations/
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_add_watsonx_jobs.sql
│   │   └── 003_add_indexes.sql
│   └── seeds/
│       └── test_data.sql
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
│
├── scripts/
│   ├── deploy.sh
│   ├── migrate.sh
│   └── test.sh
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── security-scan.yml
│
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## 12. Scalability & Performance Strategy

### 12.1 Horizontal Scaling

**Auto-scaling Configuration:**
```yaml
Metrics-based scaling:
  - CPU utilization > 70% → Scale up
  - Memory utilization > 80% → Scale up
  - Request queue depth > 100 → Scale up
  - CPU utilization < 30% for 10 min → Scale down

Scaling Limits:
  - Debugging Engine: 2-10 pods
  - Efficiency Analyzer: 2-10 pods
  - Output Formatter: 2-5 pods
  - Code Ingestion: 2-8 pods
```

### 12.2 Caching Strategy

**Multi-tier Caching:**
```
L1 (Application): In-memory cache (5 min TTL)
    ↓ Miss
L2 (Redis): Distributed cache (7 days TTL)
    ↓ Miss
L3 (PostgreSQL): Database queries
    ↓ Miss
L4 (S3): Object storage
```

**Cache Warming:**
- Pre-populate cache with common code patterns
- Predictive caching based on user history
- Background cache refresh for popular submissions

### 12.3 Database Optimization

**Query Optimization:**
- Indexed columns for frequent queries
- Materialized views for complex aggregations
- Connection pooling (max 100 connections per service)
- Read replicas for analytics queries

**Partitioning Strategy:**
```sql
-- Partition submissions by month
CREATE TABLE submissions_2026_05 PARTITION OF submissions
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
```

### 12.4 Asynchronous Processing

**Job Queue Architecture:**
```
High Priority Queue (Real-time)
  ├─ Debugging analysis
  └─ Complexity calculation

Low Priority Queue (Batch)
  ├─ watsonx refactoring
  ├─ Documentation generation
  └─ Learning path creation
```

### 12.5 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **API Response Time** | < 200ms | P95 |
| **Analysis Completion** | < 3s | P95 |
| **watsonx Operations** | < 10s | P95 |
| **Cache Hit Rate** | > 80% | Average |
| **Database Query Time** | < 50ms | P95 |
| **Throughput** | 100 req/s | Sustained |

---

## 13. Monitoring & Logging

### 13.1 Observability Stack

**Components:**
- **Metrics**: IBM Cloud Monitoring (Sysdig)
- **Logs**: IBM Log Analysis (LogDNA)
- **Traces**: IBM Cloud App Performance (Instana)
- **Alerts**: IBM Cloud Monitoring Alerts

### 13.2 Key Metrics

**Application Metrics:**
```yaml
Metrics to Track:
  - request_count (by endpoint, status)
  - request_duration_seconds (histogram)
  - analysis_execution_time_ms (histogram)
  - cache_hit_rate (gauge)
  - queue_depth (gauge)
  - error_rate (counter)
  - watsonx_api_calls (counter)
  - active_users (gauge)
```

**Infrastructure Metrics:**
```yaml
Kubernetes Metrics:
  - pod_cpu_usage
  - pod_memory_usage
  - pod_restart_count
  - node_cpu_usage
  - node_memory_usage

Database Metrics:
  - connection_pool_usage
  - query_execution_time
  - transaction_rate
  - deadlock_count
```

### 13.3 Logging Strategy

**Log Levels:**
```
ERROR: System errors, exceptions
WARN: Degraded performance, retries
INFO: Request/response, state changes
DEBUG: Detailed execution flow (dev only)
```

**Structured Logging Format:**
```json
{
  "timestamp": "2026-05-01T14:40:00Z",
  "level": "INFO",
  "service": "debugging-engine",
  "trace_id": "abc123",
  "user_id": "user456",
  "submission_id": "sub789",
  "message": "Analysis completed",
  "duration_ms": 2500,
  "metadata": {
    "language": "python",
    "bugs_found": 2
  }
}
```

### 13.4 Alerting Rules

**Critical Alerts:**
```yaml
Alerts:
  - name: HighErrorRate
    condition: error_rate > 5%
    duration: 5m
    severity: critical
    action: page_oncall
  
  - name: ServiceDown
    condition: up == 0
    duration: 1m
    severity: critical
    action: page_oncall
  
  - name: HighLatency
    condition: p95_latency > 5s
    duration: 10m
    severity: warning
    action: notify_team
  
  - name: DatabaseConnectionPoolExhausted
    condition: connection_pool_usage > 90%
    duration: 5m
    severity: warning
    action: notify_team
```

### 13.5 Distributed Tracing

**Trace Context Propagation:**
```python
# Example: Propagate trace context across services
from opentelemetry import trace
from opentelemetry.propagate import inject

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("analyze_code") as span:
    span.set_attribute("submission_id", submission_id)
    span.set_attribute("language", language)
    
    # Propagate context to downstream service
    headers = {}
    inject(headers)
    
    response = requests.post(
        "http://efficiency-analyzer/analyze",
        headers=headers,
        json=payload
    )
```

---

## 14. Future Extensibility

### 14.1 Planned Enhancements

**Phase 3: Advanced Features**
- Real-time collaborative debugging
- IDE plugins (VS Code, IntelliJ, PyCharm)
- Mobile app for on-the-go code review
- Video explanations of optimizations
- Gamification (badges, leaderboards)

**Phase 4: AI Enhancements**
- Custom model fine-tuning on user code
- Predictive bug detection before submission
- Automated test case generation
- Code smell detection
- Security vulnerability scanning

### 14.2 Language Expansion

**Roadmap:**
```
Q3 2026: JavaScript, TypeScript
Q4 2026: Go, Rust
Q1 2027: Ruby, PHP
Q2 2027: Kotlin, Swift
```

### 14.3 Integration Opportunities

**Potential Integrations:**
- GitHub Actions (CI/CD integration)
- GitLab CI (pipeline integration)
- Slack (notifications and bot)
- Microsoft Teams (collaboration)
- LeetCode/HackerRank (practice platforms)
- Coursera/Udemy (learning platforms)

### 14.4 Architecture Evolution

**Microservices Decomposition:**
```
Current: 4 core services
Future: 10+ specialized services
  - Language-specific analyzers (C++, Python, Java)
  - Specialized pattern detectors
  - ML model serving service
  - Real-time collaboration service
  - Analytics and reporting service
```

**Event-Driven Architecture:**
```
Transition from synchronous to event-driven:
  - Apache Kafka for event streaming
  - Event sourcing for audit trail
  - CQRS pattern for read/write separation
```

---

## 15. Appendix

### 15.1 Glossary

| Term | Definition |
|------|------------|
| **AST** | Abstract Syntax Tree - tree representation of code structure |
| **Big O** | Notation for describing algorithm complexity |
| **CFG** | Control Flow Graph - representation of execution paths |
| **DP** | Dynamic Programming - optimization technique |
| **IAM** | Identity and Access Management |
| **IKS** | IBM Kubernetes Service |
| **RBAC** | Role-Based Access Control |
| **SLA** | Service Level Agreement |
| **TTL** | Time To Live - cache expiration time |

### 15.2 References

- IBM watsonx.ai Documentation: https://www.ibm.com/docs/en/watsonx-as-a-service
- IBM watsonx Orchestrate: https://www.ibm.com/docs/en/watsonx/orchestrate
- IBM Cloud Kubernetes Service: https://cloud.ibm.com/docs/containers
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Redis Documentation: https://redis.io/documentation

### 15.3 Contact & Support

**Architecture Team:**
- Lead Architect: architecture@algo-coach.ibm.cloud
- DevOps Team: devops@algo-coach.ibm.cloud
- Security Team: security@algo-coach.ibm.cloud

**Support Channels:**
- Slack: #algo-coach-support
- Email: support@algo-coach.ibm.cloud
- Documentation: https://docs.algo-coach.ibm.cloud

---

**Document Version:** 1.0  
**Last Updated:** May 2026  
**Next Review:** August 2026  
**Status:** Approved for Implementation




---



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



---



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



---



# Deployment Guide

Comprehensive guide for deploying the Algorithmic Debugging & Efficiency Coach system in various environments.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [IBM Cloud Deployment](#ibm-cloud-deployment)
7. [Environment Configuration](#environment-configuration)
8. [Database Setup](#database-setup)
9. [Monitoring & Logging](#monitoring--logging)
10. [Security Configuration](#security-configuration)
11. [Scaling & Performance](#scaling--performance)
12. [Backup & Disaster Recovery](#backup--disaster-recovery)
13. [Troubleshooting](#troubleshooting)

## Overview

The system supports multiple deployment strategies:

- **Local Development**: Individual services running on localhost
- **Docker Compose**: Containerized services for development/testing
- **Kubernetes**: Production-grade orchestration with auto-scaling
- **IBM Cloud**: Fully managed deployment with IBM services

## Prerequisites

### Required Tools

```bash
# Docker & Docker Compose
docker --version  # 20.10+
docker-compose --version  # 2.0+

# Kubernetes (for K8s deployment)
kubectl version  # 1.24+
helm version  # 3.10+

# IBM Cloud CLI (for IBM Cloud deployment)
ibmcloud --version  # 2.0+
ibmcloud plugin install container-service
ibmcloud plugin install container-registry
```

### Required Accounts

- **IBM Cloud Account**: For watsonx.ai and watsonx Orchestrate
- **Container Registry**: Docker Hub, IBM Container Registry, or private registry
- **Domain & SSL**: For production deployment

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd algo-coach
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies for each service
cd services/debugging-engine
pip install -r requirements.txt

cd ../efficiency-analyzer
pip install -r requirements.txt

cd ../watsonx-ai-integration
pip install -r requirements.txt

cd ../watsonx-orchestrate-integration
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create `.env` file:

```bash
# IBM watsonx Configuration
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Service Ports
DEBUGGING_ENGINE_PORT=8001
EFFICIENCY_ANALYZER_PORT=8002
WATSONX_AI_PORT=8003
WATSONX_ORCHESTRATE_PORT=8004

# Logging
LOG_LEVEL=INFO
```

### Step 4: Start Services

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

## Docker Deployment

### Step 1: Build Docker Images

```bash
# Build all images
docker-compose build

# Or build individually
docker build -t algo-coach/debugging-engine:latest ./services/debugging-engine
docker build -t algo-coach/efficiency-analyzer:latest ./services/efficiency-analyzer
docker build -t algo-coach/watsonx-ai:latest ./services/watsonx-ai-integration
docker build -t algo-coach/watsonx-orchestrate:latest ./services/watsonx-orchestrate-integration
```

### Step 2: Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  debugging-engine:
    build: ./services/debugging-engine
    ports:
      - "8001:8001"
    environment:
      - LOG_LEVEL=INFO
      - PORT=8001
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  efficiency-analyzer:
    build: ./services/efficiency-analyzer
    ports:
      - "8002:8002"
    environment:
      - LOG_LEVEL=INFO
      - PORT=8002
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  watsonx-ai-integration:
    build: ./services/watsonx-ai-integration
    ports:
      - "8003:8003"
    environment:
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - WATSONX_PROJECT_ID=${WATSONX_PROJECT_ID}
      - WATSONX_URL=${WATSONX_URL}
      - LOG_LEVEL=INFO
      - PORT=8003
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  watsonx-orchestrate-integration:
    build: ./services/watsonx-orchestrate-integration
    ports:
      - "8004:8004"
    environment:
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - LOG_LEVEL=INFO
      - PORT=8004
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Optional: PostgreSQL for data persistence
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=algo_coach
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Optional: Redis for caching
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose down
```

### Step 4: Verify Deployment

```bash
# Check service health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

## Kubernetes Deployment

### Step 1: Create Kubernetes Manifests

Create `k8s/` directory structure:

```
k8s/
├── namespace.yaml
├── configmap.yaml
├── secrets.yaml
├── debugging-engine/
│   ├── deployment.yaml
│   └── service.yaml
├── efficiency-analyzer/
│   ├── deployment.yaml
│   └── service.yaml
├── watsonx-ai/
│   ├── deployment.yaml
│   └── service.yaml
└── watsonx-orchestrate/
    ├── deployment.yaml
    └── service.yaml
```

### Step 2: Namespace Configuration

`k8s/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: algo-coach
  labels:
    name: algo-coach
```

### Step 3: ConfigMap

`k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: algo-coach-config
  namespace: algo-coach
data:
  LOG_LEVEL: "INFO"
  WATSONX_URL: "https://us-south.ml.cloud.ibm.com"
```

### Step 4: Secrets

```bash
# Create secrets from environment variables
kubectl create secret generic algo-coach-secrets \
  --from-literal=watsonx-api-key=${WATSONX_API_KEY} \
  --from-literal=watsonx-project-id=${WATSONX_PROJECT_ID} \
  --namespace=algo-coach
```

### Step 5: Deployment Example

`k8s/debugging-engine/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debugging-engine
  namespace: algo-coach
  labels:
    app: debugging-engine
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
        image: algo-coach/debugging-engine:latest
        ports:
        - containerPort: 8001
          name: http
        env:
        - name: PORT
          value: "8001"
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: algo-coach-config
              key: LOG_LEVEL
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: debugging-engine
  namespace: algo-coach
spec:
  selector:
    app: debugging-engine
  ports:
  - port: 8001
    targetPort: 8001
    name: http
  type: ClusterIP
```

### Step 6: Horizontal Pod Autoscaler

`k8s/debugging-engine/hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: debugging-engine-hpa
  namespace: algo-coach
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: debugging-engine
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Step 7: Ingress Configuration

`k8s/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: algo-coach-ingress
  namespace: algo-coach
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.algo-coach.example.com
    secretName: algo-coach-tls
  rules:
  - host: api.algo-coach.example.com
    http:
      paths:
      - path: /debugging
        pathType: Prefix
        backend:
          service:
            name: debugging-engine
            port:
              number: 8001
      - path: /efficiency
        pathType: Prefix
        backend:
          service:
            name: efficiency-analyzer
            port:
              number: 8002
      - path: /watsonx-ai
        pathType: Prefix
        backend:
          service:
            name: watsonx-ai
            port:
              number: 8003
      - path: /watsonx-orchestrate
        pathType: Prefix
        backend:
          service:
            name: watsonx-orchestrate
            port:
              number: 8004
```

### Step 8: Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap and Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/debugging-engine/
kubectl apply -f k8s/efficiency-analyzer/
kubectl apply -f k8s/watsonx-ai/
kubectl apply -f k8s/watsonx-orchestrate/

# Deploy Ingress
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n algo-coach
kubectl get services -n algo-coach
kubectl get ingress -n algo-coach
```

## IBM Cloud Deployment

### Step 1: Set Up IBM Cloud CLI

```bash
# Login to IBM Cloud
ibmcloud login --sso

# Target resource group
ibmcloud target -g default

# Set region
ibmcloud target -r us-south
```

### Step 2: Create Kubernetes Cluster

```bash
# Create IKS cluster
ibmcloud ks cluster create classic \
  --name algo-coach-cluster \
  --zone dal10 \
  --flavor b3c.4x16 \
  --workers 3 \
  --public-vlan <vlan-id> \
  --private-vlan <vlan-id>

# Wait for cluster to be ready
ibmcloud ks cluster get --cluster algo-coach-cluster

# Configure kubectl
ibmcloud ks cluster config --cluster algo-coach-cluster
```

### Step 3: Set Up Container Registry

```bash
# Create namespace in IBM Container Registry
ibmcloud cr namespace-add algo-coach

# Build and push images
docker tag algo-coach/debugging-engine:latest \
  us.icr.io/algo-coach/debugging-engine:latest

docker push us.icr.io/algo-coach/debugging-engine:latest

# Repeat for other services
```

### Step 4: Configure watsonx Services

```bash
# Create watsonx.ai instance
ibmcloud resource service-instance-create \
  watsonx-ai watsonxai lite us-south

# Get API key
ibmcloud resource service-key-create \
  watsonx-ai-key Manager \
  --instance-name watsonx-ai

# Create watsonx Orchestrate instance
ibmcloud resource service-instance-create \
  watsonx-orchestrate watsonx-orchestrate lite us-south
```

### Step 5: Deploy to IBM Cloud

```bash
# Update image references in K8s manifests to use IBM Container Registry
# us.icr.io/algo-coach/debugging-engine:latest

# Deploy to cluster
kubectl apply -f k8s/

# Verify deployment
kubectl get all -n algo-coach
```

## Environment Configuration

### Production Environment Variables

```bash
# IBM watsonx
WATSONX_API_KEY=<production-api-key>
WATSONX_PROJECT_ID=<production-project-id>
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Database
POSTGRES_HOST=<db-host>
POSTGRES_PORT=5432
POSTGRES_DB=algo_coach_prod
POSTGRES_USER=<db-user>
POSTGRES_PASSWORD=<secure-password>

# Redis
REDIS_HOST=<redis-host>
REDIS_PORT=6379
REDIS_PASSWORD=<secure-password>

# Security
JWT_SECRET=<random-secret-key>
API_KEY_SALT=<random-salt>

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
LOG_LEVEL=INFO

# Performance
MAX_WORKERS=4
TIMEOUT=30
RATE_LIMIT=100
```

## Database Setup

### PostgreSQL Schema

```sql
-- Create database
CREATE DATABASE algo_coach_prod;

-- Create tables
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    code TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(id),
    service_name VARCHAR(100) NOT NULL,
    results JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_created_at ON submissions(created_at);
CREATE INDEX idx_analysis_submission_id ON analysis_results(submission_id);
```

## Monitoring & Logging

### Prometheus Configuration

```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'debugging-engine'
    static_configs:
      - targets: ['debugging-engine:8001']
  
  - job_name: 'efficiency-analyzer'
    static_configs:
      - targets: ['efficiency-analyzer:8002']
```

### Grafana Dashboards

Import pre-built dashboards for:
- Service health and uptime
- Request rates and latency
- Error rates
- Resource utilization

### Centralized Logging

```yaml
# fluentd-config.yaml
<source>
  @type forward
  port 24224
</source>

<match **>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
</match>
```

## Security Configuration

### SSL/TLS Setup

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: algo-coach-network-policy
  namespace: algo-coach
spec:
  podSelector:
    matchLabels:
      app: debugging-engine
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx-ingress
    ports:
    - protocol: TCP
      port: 8001
```

## Scaling & Performance

### Auto-scaling Configuration

```bash
# Enable cluster autoscaler
kubectl apply -f - <<EOF
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: debugging-engine-vpa
  namespace: algo-coach
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: debugging-engine
  updatePolicy:
    updateMode: "Auto"
EOF
```

### Performance Tuning

- Enable connection pooling
- Configure Redis caching
- Optimize database queries
- Use CDN for static assets
- Enable gzip compression

## Backup & Disaster Recovery

### Database Backup

```bash
# Automated daily backups
kubectl create cronjob postgres-backup \
  --image=postgres:15 \
  --schedule="0 2 * * *" \
  -- pg_dump -h postgres -U postgres algo_coach_prod > /backups/backup-$(date +%Y%m%d).sql
```

### Disaster Recovery Plan

1. Regular backups (daily)
2. Multi-region deployment
3. Database replication
4. Automated failover
5. Recovery time objective (RTO): 1 hour
6. Recovery point objective (RPO): 24 hours

## Troubleshooting

### Common Issues

**Pods not starting**:
```bash
kubectl describe pod <pod-name> -n algo-coach
kubectl logs <pod-name> -n algo-coach
```

**Service unreachable**:
```bash
kubectl get svc -n algo-coach
kubectl get endpoints -n algo-coach
```

**High memory usage**:
```bash
kubectl top pods -n algo-coach
kubectl describe hpa -n algo-coach
```

### Health Checks

```bash
# Check all services
for port in 8001 8002 8003 8004; do
  curl http://localhost:$port/health
done
```

---

For additional support, refer to:
- [Getting Started Guide](GETTING_STARTED.md)
- [API Reference](API_REFERENCE.md)
- [Architecture Documentation](ARCHITECTURE.md)



---



