# watsonx Orchestrate Integration Service

Workflow automation service that integrates with IBM watsonx Orchestrate for documentation updates, ticket creation, and learning path generation.

## Overview

This service automates post-analysis workflows by:
- **Documentation Updates**: Automatically updating code documentation with complexity analysis
- **Ticket Creation**: Creating refactoring tickets in Jira/GitHub based on analysis results
- **Learning Path Generation**: Generating personalized learning paths for developers based on skill gaps

## Architecture

- **Port**: 8004
- **Framework**: FastAPI
- **Integration**: IBM watsonx Orchestrate
- **Mock Mode**: Enabled by default for development

## Features

### 1. Post-Analysis Workflow
Triggered after code analysis completes:
- Updates documentation with complexity findings
- Creates tickets for identified issues
- Sends notifications to stakeholders

### 2. Optimization Workflow
Triggered when optimization is applied:
- Updates documentation with new complexity
- Closes related tickets
- Logs performance improvements

### 3. Developer Growth Workflow
Triggered periodically or on-demand:
- Analyzes historical code submissions
- Identifies skill gaps
- Generates personalized learning paths
- Schedules follow-up assessments

## API Endpoints

### Health Check
```bash
GET /health
```

### Trigger Workflow
```bash
POST /workflow/trigger
Content-Type: application/json

{
  "workflow_type": "post_analysis",
  "analysis_results": {
    "file_path": "src/algorithms/sort.py",
    "complexity": {"time": "O(n^2)", "space": "O(1)"},
    "issues": ["nested loops", "inefficient sorting"]
  },
  "developer_id": "dev123",
  "project_id": "proj456"
}
```

### Get Workflow Status
```bash
GET /workflow/status/{job_id}
```

### Webhook Handler
```bash
POST /webhook
Content-Type: application/json

{
  "event_type": "ticket_created",
  "payload": {"ticket_id": "PROJ-123"},
  "source": "jira",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
export ORCHESTRATE_API_KEY="your-api-key"
export ORCHESTRATE_API_URL="https://api.orchestrate.ibm.com"
export ORCHESTRATE_MOCK_MODE="false"  # Set to false for production
export TICKETING_SYSTEM="jira"  # or "github"
export TICKETING_API_TOKEN="your-token"
export TICKETING_PROJECT_KEY="PROJ"
```

3. Run the service:
```bash
python -m app.handler
```

The service will start on `http://localhost:8004`

### Docker Deployment

```bash
docker build -t watsonx-orchestrate-integration .
docker run -p 8004:8004 watsonx-orchestrate-integration
```

## Configuration

### Mock Mode
By default, the service runs in mock mode for development:
- Simulates watsonx Orchestrate API responses
- Generates mock tickets and documentation
- No actual API calls are made

To disable mock mode:
```bash
export ORCHESTRATE_MOCK_MODE="false"
export TICKETING_MOCK_MODE="false"
export DOCS_MOCK_MODE="false"
```

### Ticketing System Integration

#### Jira
```bash
export TICKETING_SYSTEM="jira"
export TICKETING_API_URL="https://your-domain.atlassian.net"
export TICKETING_API_TOKEN="your-jira-token"
export TICKETING_PROJECT_KEY="PROJ"
```

#### GitHub Issues
```bash
export TICKETING_SYSTEM="github"
export TICKETING_API_TOKEN="your-github-token"
export TICKETING_PROJECT_KEY="owner/repo"
```

## Usage Examples

### Example 1: Post-Analysis Workflow

```python
import requests

response = requests.post("http://localhost:8004/workflow/trigger", json={
    "workflow_type": "post_analysis",
    "analysis_results": {
        "file_path": "src/algorithms/sort.py",
        "complexity": {
            "time_complexity": "O(n^2)",
            "space_complexity": "O(1)"
        },
        "issues": [
            "Inefficient nested loops",
            "Missing edge case handling"
        ],
        "suggestions": [
            "Replace bubble sort with merge sort",
            "Add input validation"
        ]
    },
    "developer_id": "dev123",
    "project_id": "proj456"
})

job_id = response.json()["job_id"]
print(f"Workflow started: {job_id}")
```

### Example 2: Optimization Workflow

```python
response = requests.post("http://localhost:8004/workflow/trigger", json={
    "workflow_type": "optimization",
    "analysis_results": {
        "file_path": "src/algorithms/sort.py",
        "before_complexity": {"time": "O(n^2)", "space": "O(1)"},
        "after_complexity": {"time": "O(n log n)", "space": "O(n)"},
        "changes_made": ["Replaced bubble sort with merge sort"],
        "performance_improvement": {"percentage": 75}
    },
    "developer_id": "dev123",
    "project_id": "proj456"
})
```

### Example 3: Developer Growth Workflow

```python
response = requests.post("http://localhost:8004/workflow/trigger", json={
    "workflow_type": "developer_growth",
    "analysis_results": {
        "submissions": [
            {"file": "solution1.py", "issues": ["inefficient DP"]},
            {"file": "solution2.py", "issues": ["poor graph traversal"]}
        ],
        "skill_level": "intermediate"
    },
    "developer_id": "dev123",
    "project_id": "proj456"
})
```

## Testing

Run the test suite:
```bash
python test_service.py
```

## Project Structure

```
watsonx-orchestrate-integration/
├── app/
│   ├── __init__.py
│   ├── handler.py              # Main FastAPI application
│   ├── models/
│   │   ├── request.py          # Request models
│   │   └── response.py         # Response models
│   ├── services/
│   │   ├── orchestrate_client.py  # watsonx Orchestrate client
│   │   ├── documentation.py       # Documentation service
│   │   ├── ticketing.py           # Ticketing service
│   │   └── learning_path.py       # Learning path service
│   ├── workflows/
│   │   ├── post_analysis.py       # Post-analysis workflow
│   │   ├── optimization.py        # Optimization workflow
│   │   └── developer_growth.py    # Developer growth workflow
│   └── utils/
│       └── logger.py              # Logging configuration
├── requirements.txt
├── Dockerfile
├── test_service.py
└── README.md
```

## Integration with Other Services

This service integrates with:
- **Debugging Engine** (port 8001): Receives analysis results
- **Efficiency Analyzer** (port 8002): Receives complexity analysis
- **watsonx.ai Integration** (port 8003): Triggers AI-powered content generation

## Mock vs Production Mode

### Mock Mode (Development)
- No actual API credentials required
- Simulates all external API calls
- Generates realistic mock responses
- Logs what would be sent to real APIs

### Production Mode
- Requires valid API credentials
- Makes actual API calls to watsonx Orchestrate
- Creates real tickets in Jira/GitHub
- Updates actual documentation files

## Troubleshooting

### Service won't start
- Check if port 8004 is available
- Verify Python version (3.11+)
- Ensure all dependencies are installed

### Workflows fail
- Check logs for detailed error messages
- Verify API credentials if not in mock mode
- Ensure analysis results have required fields

### Tickets not created
- Verify ticketing system configuration
- Check API token permissions
- Review mock mode settings

## License

IBM Confidential

## Support

For issues or questions, contact the development team.