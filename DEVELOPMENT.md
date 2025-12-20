# Development Guide

This guide covers how to set up and work on the `nestedutils` project locally.

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - A fast Python package installer and resolver

## Installation

### Installing uv

If you don't have `uv` installed, you can install it using [UV Getting Started](https://docs.astral.sh/uv/getting-started/installation/)

### Setting Up the Development Environment

1. Clone the repository:

```bash
git clone https://github.com/ysskrishna/nestedutils.git
cd nestedutils
```

2. Install the project and development dependencies using `uv`:

```bash
uv sync --dev
```

This will:
- Create a virtual environment (if it doesn't exist)
- Install the project in editable mode
- Install all development dependencies (including `pytest`)

## Local Testing

### Running Tests

Run all tests using pytest:

```bash
uv run pytest
```

### Running Specific Test Files

```bash
uv run pytest tests/test_get.py
```

### Building the Package

To build the package locally:

```bash
uv build
```

This will create distribution files in the `dist/` directory:

- `nestedutils-<version>-py3-none-any.whl` (wheel)
- `nestedutils-<version>.tar.gz` (source distribution)

### Installing the Local Package

To test the package installation locally:

```bash
# Install from the built wheel
uv pip install dist/nestedutils-*.whl

# Or install in editable mode for development
uv pip install -e .
```

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Packaging Guide](https://packaging.python.org/)
