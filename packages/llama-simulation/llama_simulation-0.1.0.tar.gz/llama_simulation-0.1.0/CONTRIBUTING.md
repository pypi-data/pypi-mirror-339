# Contributing to llama_simulation

Thank you for considering contributing to llama_simulation! This document outlines the process for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read it before contributing.

## How to Contribute

### Reporting Bugs

If you find a bug in the codebase, please submit an issue to our GitHub repository. When submitting an issue, please include:

- A clear, descriptive title
- A detailed description of the bug
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment information (OS, Python version, package version)

### Suggesting Features

Feature suggestions are welcome! Please submit an issue with the following:

- A clear, descriptive title
- A detailed description of the proposed feature
- Any relevant examples or mock-ups
- Potential implementation approaches

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes
4. Run tests: `pytest`
5. Format your code: `black .` and `isort .`
6. Submit a pull request to the `main` branch

## Development Guidelines

### Setting Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/llama_simulation.git
cd llama_simulation

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Style

We follow the PEP 8 style guide with a few modifications:

- Line length: 100 characters
- Use Google-style docstrings
- Use type hints

We use the following tools for code quality:

- Black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

### Testing

Write tests for all new code. We use pytest for testing.

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=llama_simulation

# Run specific tests
pytest tests/test_simulation_lab.py
```

### Documentation

Document all public modules, functions, classes, and methods. We use Google-style docstrings.

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

Types include:
- feat: new feature
- fix: bug fix
- docs: documentation change
- style: code style change
- refactor: code refactoring
- test: adding tests
- chore: maintenance tasks

### Pull Request Process

1. Update the README.md with details of changes if applicable.
2. Update the CHANGELOG.md with details of changes.
3. Ensure all tests pass and code quality checks pass.
4. The PR will be merged once it receives approval from maintainers.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
