# Contributing to QuantumAlpha

Thank you for your interest in contributing to QuantumAlpha! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
  - [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Commit Messages](#commit-messages)
  - [Pull Requests](#pull-requests)
  - [Code Reviews](#code-reviews)
- [Coding Standards](#coding-standards)
  - [Python](#python)
  - [JavaScript/TypeScript](#javascripttypescript)
  - [Documentation](#documentation)
- [Testing](#testing)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Development Environment

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/QuantumAlpha.git
   cd QuantumAlpha
   ```

2. **Set Up Development Environment**

   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Set up pre-commit hooks
   pre-commit install
   ```

3. **Set Up Frontend Development**

   ```bash
   # Web Frontend
   cd web-frontend
   npm install

   # Mobile Frontend
   cd ../mobile-frontend
   npm install
   ```

### Project Structure

The project is organized as follows:

```
QuantumAlpha/
├── backend/               # Backend services
│   ├── data-service/      # Data ingestion and processing
│   ├── ai-engine/         # ML/AI models and training
│   ├── risk-service/      # Risk management
│   └── execution-service/ # Trading execution
├── web-frontend/          # Web dashboard
├── mobile-frontend/       # Mobile app
├── infrastructure/        # Deployment configurations
├── config/                # Configuration files
├── docs/                  # Documentation
└── tests/                 # Test suite
```

## Development Workflow

### Branching Strategy

We follow a Git Flow-inspired branching strategy:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent fixes for production
- `release/*`: Release preparation

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or modifying tests
- `build`: Build system changes
- `ci`: CI configuration changes
- `chore`: Other changes

Examples:

```
feat(ai-engine): add support for transformer models
fix(data-service): resolve connection timeout with external APIs
docs: update installation instructions
```

### Pull Requests

1. Create a new branch from `develop` for your changes
2. Make your changes and commit them with descriptive messages
3. Push your branch to your fork
4. Open a pull request against the `develop` branch
5. Fill out the pull request template
6. Wait for code review and address any feedback

### Code Reviews

All submissions require review. We use GitHub pull requests for this purpose.

- Be respectful and constructive in reviews
- Focus on code quality, not style preferences
- Explain the reasoning behind your suggestions
- Approve once all issues are addressed

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Use [mypy](https://mypy.readthedocs.io/) for type checking
- Write docstrings in [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### JavaScript/TypeScript

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use ESLint and Prettier for code formatting
- Use TypeScript for type safety
- Write JSDoc comments for functions and classes

### Documentation

- Write clear, concise documentation
- Use Markdown for documentation files
- Document all public APIs
- Include examples where appropriate
- Keep documentation up-to-date with code changes

## Testing

- Write tests for all new features and bug fixes
- Maintain or improve test coverage
- Run the test suite before submitting a pull request
- Write unit tests, integration tests, and end-to-end tests as appropriate

```bash
# Run backend tests
pytest

# Run frontend tests
cd web-frontend
npm test
```

## Reporting Issues

- Use the GitHub issue tracker
- Check if the issue already exists before creating a new one
- Follow the issue template
- Provide as much detail as possible
- Include steps to reproduce, expected behavior, and actual behavior

## Feature Requests

- Use the GitHub issue tracker with the "enhancement" label
- Clearly describe the feature and its benefits
- Consider the scope and impact of the feature
- Discuss implementation details if possible

## Community

- Join our [Discord server](https://discord.gg/example) for discussions
- Subscribe to our [mailing list](https://example.com/mailing-list)
- Follow us on [Twitter](https://twitter.com/example)
- Participate in community calls and events

Thank you for contributing to QuantumAlpha!
