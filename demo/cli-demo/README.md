# CLI Demo Application

Interactive command-line interface for demonstrating the Algorithmic Debugging & Efficiency Coach system.

## Overview

This CLI application provides an easy-to-use interface for testing and demonstrating the capabilities of the system, including:

- Code debugging analysis
- Efficiency and complexity analysis
- Code refactoring with watsonx.ai
- Automated workflow actions with watsonx Orchestrate

## Features

- **Interactive Menu System**: User-friendly navigation
- **Example Code Analysis**: Pre-loaded examples demonstrating various issues
- **Custom Code Analysis**: Analyze your own code
- **Service Health Monitoring**: Check status of all microservices
- **Colored Output**: Clear, formatted results with syntax highlighting
- **Multiple Language Support**: Python, C++, and Java

## Prerequisites

- Python 3.8 or higher
- All microservices running:
  - Debugging Engine (port 8001)
  - Efficiency Analyzer (port 8002)
  - watsonx.ai Integration (port 8003)
  - watsonx Orchestrate Integration (port 8004)

## Installation

1. Navigate to the CLI demo directory:
```bash
cd demo/cli-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the CLI

```bash
python app.py
```

### Menu Options

1. **Analyze Example Code (Buggy Python)**: Demonstrates debugging capabilities with intentionally buggy code
2. **Analyze Example Code (Inefficient Python)**: Shows efficiency analysis on O(n²) code
3. **Analyze Custom Code**: Submit your own code for analysis
4. **View Example Files**: Browse available example code files
5. **Check Service Health**: Verify all microservices are running
6. **About This System**: Learn about the system architecture and features
0. **Exit**: Close the application

### Analyzing Custom Code

When selecting option 3:

1. Choose the programming language (Python, C++, or Java)
2. Select input method:
   - Enter code directly (end with Ctrl+D on Unix/Linux or Ctrl+Z on Windows)
   - Load from a file (provide file path)
3. View comprehensive analysis results

## Example Files

The `examples/` directory contains three demonstration files:

### buggy_code.py
Contains multiple intentional bugs:
- Syntax errors (missing colons)
- Logic errors (off-by-one errors)
- Runtime errors (division by zero, index out of bounds)

### inefficient_code.py
Demonstrates inefficient algorithms:
- O(n²) time complexity with nested loops
- Inefficient pattern: checking membership in lists
- Can be optimized to O(n) using hash maps/sets

### optimized_code.py
Shows optimized implementations:
- O(n) time complexity
- Efficient use of data structures (sets, dictionaries)
- Best practices for algorithm design

## Output Format

The CLI displays results in the following structure:

```
=== DIAGNOSTIC SUMMARY ===
[Bug descriptions and explanations]

=== COMPLEXITY BREAKDOWN ===
Current Time Complexity: O(n²)
Current Space Complexity: O(n)
Target Time Complexity: O(n)
Target Space Complexity: O(n)

=== THE OPTIMIZATION PATH ===
Step 1: [Conceptual guide]
Step 2: [Conceptual guide]
...

=== AUTOMATED ACTIONS ===
✓ Documentation updated: [file paths]
✓ Tickets created: [ticket IDs]
✓ Learning path generated: [topics]

=== REFACTORED CODE ===
[Optimized code with explanation]
```

## Architecture

The CLI application consists of:

```
demo/cli-demo/
├── app.py                    # Main CLI application
├── services/
│   ├── __init__.py
│   ├── api_client.py         # API client for microservices
│   └── formatter.py          # Output formatting
├── examples/
│   ├── buggy_code.py         # Example with bugs
│   ├── inefficient_code.py   # Example with O(n²) complexity
│   └── optimized_code.py     # Optimized O(n) code
├── requirements.txt
└── README.md
```

## API Client

The `api_client.py` module provides methods to interact with all microservices:

- `analyze_debugging()`: Submit code to debugging engine
- `analyze_efficiency()`: Submit code to efficiency analyzer
- `generate_refactored_code()`: Request code refactoring from watsonx.ai
- `trigger_automated_actions()`: Trigger watsonx Orchestrate workflows
- `complete_analysis()`: Perform full analysis pipeline
- `health_check()`: Check service availability

## Troubleshooting

### Services Not Available

If you see "Service unavailable" errors:

1. Check that all microservices are running:
```bash
# Check debugging engine
curl http://localhost:8001/health

# Check efficiency analyzer
curl http://localhost:8002/health

# Check watsonx.ai integration
curl http://localhost:8003/health

# Check watsonx Orchestrate integration
curl http://localhost:8004/health
```

2. Start any missing services:
```bash
# Start debugging engine
cd services/debugging-engine
python -m app.main

# Start efficiency analyzer
cd services/efficiency-analyzer
python -m app.main

# Start watsonx.ai integration
cd services/watsonx-ai-integration
python -m app.handler

# Start watsonx Orchestrate integration
cd services/watsonx-orchestrate-integration
python -m app.handler
```

### Import Errors

If you encounter import errors:

```bash
# Ensure you're in the correct directory
cd demo/cli-demo

# Reinstall dependencies
pip install -r requirements.txt
```

### Color Display Issues on Windows

If colors don't display correctly on Windows:

```bash
# Colorama should handle this automatically, but if issues persist:
pip install --upgrade colorama
```

## Development

### Adding New Examples

To add new example files:

1. Create a new file in `examples/` directory
2. Add appropriate comments explaining the issues
3. Update the CLI menu if needed

### Customizing Output Format

Modify `services/formatter.py` to customize:
- Color schemes
- Output structure
- Display formatting

### Extending API Client

Add new methods to `services/api_client.py` to support:
- Additional endpoints
- New analysis types
- Custom workflows

## Related Documentation

- [Project Summary](../../PROJECT_SUMMARY.md)
- [Getting Started Guide](../../GETTING_STARTED.md)
- [API Reference](../../API_REFERENCE.md)
- [Architecture Documentation](../../ARCHITECTURE.md)

## Support

For issues or questions:
- Check the main project README
- Review service-specific documentation
- Verify all services are running and accessible

## License

Part of the Algorithmic Debugging & Efficiency Coach project.