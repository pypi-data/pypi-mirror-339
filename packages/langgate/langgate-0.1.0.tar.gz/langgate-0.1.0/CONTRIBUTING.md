# Contributing to LangGate

This document provides instructions for setting up and contributing to the LangGate project.

## Workspace Structure

LangGate is organized as a uv workspace with multiple packages using a PEP-420 namespace package structure:

```
/
├── pyproject.toml            # Main project configuration with workspace definition
├── packages/
│   ├── core/                 # Core shared models and utilities
│   │   └── src/
│   │       └── langgate/
│   │           └── core/
│   ├── client/               # HTTP client for remote registry
│   │   └── src/
│   │       └── langgate/
│   │           └── client/
│   ├── registry/             # Registry for model information
│   │   └── src/
│   │       └── langgate/
│   │           └── registry/
│   ├── transform/            # Parameter transformation logic
│   │   └── src/
│   │       └── langgate/
│   │           └── transform/
│   ├── processor/            # Envoy external processor implementation
│   │   └── src/
│   │       └── langgate/
│   │           └── processor/
│   ├── server/               # API server implementation
│   │   └── src/
│   │       └── langgate/
│   │           └── server/
│   └── sdk/                  # Convenience package combining registry and transform
│       └── src/
│           └── langgate/
│               └── sdk/
├── examples/                 # Example usage of the SDK components
├── services/                 # Service-specific configurations
└── docs/                     # Documentation
```

Each package can be developed and published independently, while also working together through the shared `langgate` namespace. This PEP-420 namespace package structure allows for clean imports like `from langgate.core import X` or `from langgate.registry import Y`.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tanantor/langgate.git
   cd langgate
   ```

2. **Set up the development environment**:
   ```bash
   make sync
   ```

   This will create a virtual environment with all dependencies installed.

## Working with the Workspace

### Running Tests

Run tests from the project root:

```bash
make test
```

### Linting and Type Checking

Before submitting changes, run linting and type checking:

```bash
make lint
make mypy
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions and methods
- Include docstrings for all public functions, classes, and methods
- Strictly adhere to SOLID principles

## Pull Request Process

1. Create a branch for your changes
2. Make your changes
3. Ensure tests pass
4. Run linting and type checking
5. Submit a pull request

## Release Process

LangGate follows semantic versioning for all releases.

### Release Preparation

Prior to a release, a PR should be created that:

1. Updates the version in `pyproject.toml`
2. Updates versions in Helm charts (`deployment/k8s/charts/*/Chart.yaml`)
3. Updates `CHANGELOG.md` with a summary of changes

### Creating a Release

After the version bump PR is merged:

1. Create a release tag:
   - Create and push a tag matching the version: `git tag v0.1.0 && git push origin v0.1.0`
   - This will automatically trigger the release workflow

2. The release process automatically:
   - Creates a GitHub release
   - Publishes Python packages to PyPI
   - Publishes Docker images to GitHub Container Registry
   - Publishes Helm charts

3. Alternatively, a release can be manually triggered:
   - Go to Actions → Create GitHub Release workflow
   - Enter the version number (without 'v' prefix)
   - Run the workflow

### Published Artifacts

- **PyPI Packages**: `pip install langgate`
- **Docker Images**:
  - `ghcr.io/tanantor/langgate-server:VERSION`
  - `ghcr.io/tanantor/langgate-processor:VERSION`
  - `ghcr.io/tanantor/langgate-envoy:VERSION`
- **Helm Charts**: `helm repo add langgate https://tanantor.github.io/langgate/charts`

Thank you for contributing to LangGate!
