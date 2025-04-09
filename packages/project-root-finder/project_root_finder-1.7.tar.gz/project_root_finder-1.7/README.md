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

This test suite comprehensively verifies the behaviour of `_get_project_root`, ensuring it correctly identifies the project root directory under a variety of conditions.

The tests cover the following scenarios:

| Test Name | Purpose | What it Verifies |
|:----------|:--------|:-----------------|
| `test_finds_project_root_hook` | Priority on `.project-root-hook` | Ensures the function correctly identifies the root when `.project-root-hook` is present, even from nested folders. |
| `test_fallback_to_git` | Fallback to `.git` marker | Ensures that if `.project-root-hook` is missing, the function falls back correctly to detecting a `.git` directory. |
| `test_fallback_to_pipfile` | Fallback to `Pipfile` marker | Checks fallback behaviour when a `Pipfile` exists instead of `.project-root-hook`. |
| `test_fallback_to_pyproject_toml` | Fallback to `pyproject.toml` | Verifies that `pyproject.toml` is correctly recognised as a valid project root marker if no hook is present. |
| `test_no_marker_returns_none` | No markers at all | Confirms that the function returns `None` gracefully if no valid markers are found. |
| `test_custom_start_path_at_root` | Start directly at root | Ensures that starting the search from the root itself works correctly and immediately finds the root. |
| `test_multiple_markers_prefers_project_hook` | Priority over fallback markers | Verifies that `.project-root-hook` is prioritised over any fallback markers like `.git`, even if both are present. |
| `test_fallback_order_is_respected` | Correct fallback order | Ensures that when multiple fallback markers exist, the function still correctly identifies the root without confusion. |
| `test_deeply_nested_still_finds_root` | Deep directory traversal | Checks that even when called from a very deeply nested directory (10 levels down), the root is still correctly found by traversing upwards. |

---
