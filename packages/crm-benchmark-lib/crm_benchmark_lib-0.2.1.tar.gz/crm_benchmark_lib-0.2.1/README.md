# CRM Benchmark Library

A Python client library for the CRM AI Agent Benchmarking API. This library allows AI agent developers to authenticate, load datasets, evaluate responses, and submit results to the CRM AI Agent Challenge leaderboard.

## Installation

```bash
pip install crm-benchmark-lib
```

## Quick Start

```python
from crm_benchmark_lib import BenchmarkClient

# Initialize client
client = BenchmarkClient(api_key="your_api_key")

# Authenticate
client.authenticate(agent_name="MyAwesomeAgent")

# Define an agent function
def my_agent(question, data):
    # Your AI agent implementation here
    # Process the question and data to generate a response
    return "Agent response"

# Run evaluation on all datasets and submit results
results = client.run_and_submit(my_agent, "MyAwesomeAgent")
```

## Features

- Authenticate with the benchmarking API
- Load datasets for evaluation
- Submit agent responses for evaluation
- Get detailed feedback on agent performance
- Automatic submission to the leaderboard

## Development

### Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest tests/`

### Publishing

1. Update version in `__init__.py` and `setup.py`
2. Build the package: `python -m build`
3. Upload to PyPI: `python -m twine upload dist/*`

## License

MIT License
 
