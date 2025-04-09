# project_root_finder

`project_root_finder` is a simple Python package that provides a variable `root` which represents the absolute path to the root of the project in which it is installed.

## Installation

You can install the package using pip:

```bash
pip install project_root_finder
```

## Usage Examples

The `project_root_finder` package provides a simple way to get the absolute path to your project's root directory. This is useful for file operations that need to be relative to your project root, regardless of where the script is executed from.

### Basic Usage

```python
import project_root_finder
from pathlib import Path

# Access the project root path (returns a Path object)
project_root = project_root_finder.root

# Use it for file operations with pathlib
config_path = project_root / "config" / "settings.yaml"
data_path = project_root / "data" / "samples.csv"

# Or convert to string for other operations
log_path = str(project_root / "logs" / "application.log")
```

### How It Works

The package determines the project root by:

1. Starting from the location of its own `__init__.py` file
2. Searching upward through parent directories for common project marker files:
   - `.git` (Git repository)
   - `pyproject.toml` (Python project config)
   - `setup.py` (Python package setup)
   - `Pipfile` (Pipenv configuration)
3. If a marker is found, that directory is used as the project root
4. If no markers are found in any parent directories, it falls back to the parent directory of the module

### Custom Project Root Marker

The `project_root_finder` package also supports a custom project root marker file named `.project-root-hook`. If this file is present in any parent directory of the starting path, it will take precedence over other markers (e.g., `.git`, `pyproject.toml`, etc.) when determining the project root.

This feature is useful for projects that do not use standard markers or require a specific marker to define the root directory.

## Running Tests

This package includes a comprehensive test suite to ensure it works correctly across different scenarios.

### Prerequisites

Make sure you have the development dependencies installed:

```bash
pip install pytest
# Or if using pipenv
pipenv install --dev
```

### Running the Tests

To run the test suite:

```bash
pytest
```

Or for more verbose output:

```bash
pytest -v
```

### What the Tests Cover

The test suite verifies that `project_root_finder`:

1. Returns a proper Path object
2. Always returns an absolute path
3. Correctly identifies project roots by detecting project marker files
4. Falls back to the package's parent directory when no markers are found
5. Properly checks all supported project markers in each parent directory

The tests use mocking to simulate different directory structures without requiring actual filesystem changes.
