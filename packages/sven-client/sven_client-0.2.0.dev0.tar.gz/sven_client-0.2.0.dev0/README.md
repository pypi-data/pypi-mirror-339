# Sven

Sven is the CLI client for ActiveAgent, providing a command-line interface for interacting with the ActiveAgent server.

## Installation

```bash
pip install sven
```

## Usage

```bash
# Basic usage
sven --help

# Connect to a server
sven client --url http://localhost:8000

# Run an agent
sven agent run --name my-agent

# List available tools
sven tools list

# Store question-answer pairs
sven qa store --file examples/qa_example.json

# Query the question-answer database
sven qa query "How do I create a branch in Git?"
```

## Configuration

Sven can be configured using a YAML configuration file. Create a `.sven.yml` file in your home directory or project directory:

```yaml
api_url: "https://api.swedishembedded.com"
api_port: 443
api_key: "your-api-key-here"
model: "claude-3-7-sonnet-latest"
persona: "coder"
```

See the [configuration documentation](docs/configuration.md) for more details on how to configure Sven and provide API keys.

## Features

### Question-Answer Database

Sven provides commands to interact with a semantic question-answer database:

```bash
# Store question-answer pairs from a JSON or YAML file
sven qa store --file examples/qa_example.json

# Query the database using semantic search
sven qa query "How do I create a branch in Git?"
```

The questions and answers are organized into categories and can include metadata. See the example files in the `examples/` directory for the correct format:

- [JSON Example](examples/qa_example.json)
- [YAML Example](examples/qa_example.yaml)

## Development

### Setup

```bash
# Clone the repository
git clone https://git.swedishembedded.com/core/platform/sven.git
cd sven

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
pytest
```

### Linting

```bash
# Run all linters
pre-commit run --all-files

# Run individual linters
black .
isort .
mypy .
ruff .
```

### CI/CD Pipeline

This project uses GitLab CI/CD for automated testing, building, and deployment. The pipeline includes:

- **Lint**: Code quality checks with black, isort, ruff, and mypy
- **Test**: Unit and integration tests with pytest
- **Build**: Package building with setuptools
- **Publish**: Publishing to PyPI (on tags) and TestPyPI (on main branch)

### Releasing

We use semantic versioning for this project. To create a new release:

1. Update the CHANGELOG.md with your changes
2. Use bump2version to increment the version:
   ```bash
   # For a patch release (0.1.0 -> 0.1.1)
   bump2version patch

   # For a minor release (0.1.0 -> 0.2.0)
   bump2version minor

   # For a major release (0.1.0 -> 1.0.0)
   bump2version major
   ```
3. Push the new tag to trigger the release pipeline:
   ```bash
   git push --tags
   ```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

MIT
