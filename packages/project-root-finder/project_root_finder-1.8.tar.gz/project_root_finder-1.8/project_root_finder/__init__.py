from pathlib import Path

def _get_project_root(start_path=None, marker_filename=".project-root-hook"):
    if start_path is None:
        path = Path.cwd()
    else:
        path = Path(start_path).resolve()

    fallback_markers = [
        '.git',         # Git repository
        'Pipfile',      # Pipenv projects
        'pyproject.toml', # Poetry or modern Python projects
        'requirements.txt', # Traditional virtualenv-based projects
    ]

    for parent in [path] + list(path.parents):
        # First priority: .project-root-hook
        if (parent / marker_filename).is_file():
            return parent

    # If we get here, no .project-root-hook was found
    for parent in [path] + list(path.parents):
        if any((parent / marker).exists() for marker in fallback_markers):
            return parent

    return None

root = _get_project_root()

__all__ = ["root"]