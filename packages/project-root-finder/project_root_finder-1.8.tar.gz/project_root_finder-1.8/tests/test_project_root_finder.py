import pytest
from project_root_finder import _get_project_root


def create_file(path, name):
    """Helper to create a file at a given path."""
    file_path = path / name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch()
    return file_path

def test_finds_project_root_hook(tmp_path):
    """Test finding .project-root-hook at the root."""
    create_file(tmp_path, '.project-root-hook')
    nested = tmp_path / 'a' / 'b'
    nested.mkdir(parents=True)
    found = _get_project_root(start_path=nested)
    assert found == tmp_path

def test_fallback_to_git(tmp_path):
    """Test fallback to .git if no project-root-hook."""
    create_file(tmp_path, '.git')
    nested = tmp_path / 'src'
    nested.mkdir()
    found = _get_project_root(start_path=nested)
    assert found == tmp_path

def test_fallback_to_pipfile(tmp_path):
    """Test fallback to Pipfile if no project-root-hook."""
    create_file(tmp_path, 'Pipfile')
    nested = tmp_path / 'module'
    nested.mkdir()
    found = _get_project_root(start_path=nested)
    assert found == tmp_path

def test_fallback_to_pyproject_toml(tmp_path):
    """Test fallback to pyproject.toml."""
    create_file(tmp_path, 'pyproject.toml')
    nested = tmp_path / 'lib'
    nested.mkdir()
    found = _get_project_root(start_path=nested)
    assert found == tmp_path

def test_no_marker_returns_none(tmp_path):
    """Test when no markers exist, should return None."""
    nested = tmp_path / 'no_marker'
    nested.mkdir(parents=True)
    found = _get_project_root(start_path=nested)
    assert found is None

def test_custom_start_path_at_root(tmp_path):
    """Test if starting directly at the project root."""
    create_file(tmp_path, '.project-root-hook')
    found = _get_project_root(start_path=tmp_path)
    assert found == tmp_path

def test_multiple_markers_prefers_project_hook(tmp_path):
    """Test it prefers .project-root-hook over fallbacks."""
    create_file(tmp_path, '.git')
    create_file(tmp_path, '.project-root-hook')
    nested = tmp_path / 'deep'
    nested.mkdir()
    found = _get_project_root(start_path=nested)
    assert found == tmp_path

def test_fallback_order_is_respected(tmp_path):
    """Test fallback order when multiple fallback markers exist but no project hook."""
    create_file(tmp_path, 'Pipfile')
    create_file(tmp_path, 'setup.py')  # multiple markers
    nested = tmp_path / 'src'
    nested.mkdir()
    found = _get_project_root(start_path=nested)
    assert found == tmp_path

def test_deeply_nested_still_finds_root(tmp_path):
    """Test that deep nested directories still correctly find the project root."""
    create_file(tmp_path, '.project-root-hook')

    # Create a deep folder structure
    deep_path = tmp_path
    for part in range(10):  # 10 levels deep
        deep_path = deep_path / f'level_{part}'
        deep_path.mkdir()

    found = _get_project_root(start_path=deep_path)
    assert found == tmp_path