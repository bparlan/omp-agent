#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-PROJECT_ROOT_DETECTION}
# Test Type: IMPLEMENTATION_CHECK

import pytest
import tempfile
import os
from pathlib import Path


def test_find_project_root_resolves_to_nearest_marker_bearing_ancestor():
    """VI-3: find_project_root resolves to nearest marker-bearing ancestor."""

    # Import the module under test
    from discovery import find_project_root

    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Create skills/ marker case
        skills_case = root / "skills"
        skills_case.mkdir()
        (skills_case / "some_file.txt").touch()

        deep_skills_dir = skills_case / "level1" / "level2" / "deep"
        deep_skills_dir.mkdir(parents=True)
        (deep_skills_dir / "test.txt").touch()

        # Test skills/ marker
        result = find_project_root(deep_skills_dir)
        assert isinstance(result, Path), f"Expected Path, got {type(result)}"
        assert result.is_absolute(), f"Expected absolute path, got {result}"
        assert result.exists(), f"Expected existing path, got {result}"
        assert result.is_dir(), f"Expected directory, got {result}"
        assert result == root.resolve(), f"Expected {root.resolve()}, got {result}"

        # Create package.json marker case
        pkg_case = root / "package.json"
        pkg_case.touch()
        deep_pkg_dir = root / "subdir" / "subsubdir" / "deeper"
        deep_pkg_dir.mkdir(parents=True)
        (deep_pkg_dir / "test.txt").touch()

        result = find_project_root(deep_pkg_dir)
        assert isinstance(result, Path), f"Expected Path, got {type(result)}"
        assert result.is_absolute(), f"Expected absolute path, got {result}"
        assert result.exists(), f"Expected existing path, got {result}"
        assert result.is_dir(), f"Expected directory, got {result}"
        assert result == root.resolve(), f"Expected {root.resolve()}, got {result}"

        # Create pyproject.toml marker case
        pyproj_case = root / "pyproject.toml"
        pyproj_case.touch()
        deep_pyproj_dir = root / "nested" / "structure" / "here"
        deep_pyproj_dir.mkdir(parents=True)
        (deep_pyproj_dir / "test.txt").touch()

        result = find_project_root(deep_pyproj_dir)
        assert isinstance(result, Path), f"Expected Path, got {type(result)}"
        assert result.is_absolute(), f"Expected absolute path, got {result}"
        assert result.exists(), f"Expected existing path, got {result}"
        assert result.is_dir(), f"Expected directory, got {result}"
        assert result == root.resolve(), f"Expected {root.resolve()}, got {result}"


def test_find_project_root_default_argument_resolves_to_absolute_path_cwd():
    """VI-4: find_project_root default argument resolves to absolute Path.cwd()."""

    # Import the module under test
    from discovery import find_project_root

    # Test with no arguments
    result_no_args = find_project_root()

    # Test with None argument
    result_none_args = find_project_root(None)

    # Verify both return the same absolute path
    import os
    expected_cwd = Path.cwd().resolve()

    assert isinstance(result_no_args, Path), f"Expected Path, got {type(result_no_args)}"
    assert isinstance(result_none_args, Path), f"Expected Path, got {type(result_none_args)}"

    assert result_no_args.is_absolute(), f"Expected absolute path, got {result_no_args}"
    assert result_none_args.is_absolute(), f"Expected absolute path, got {result_none_args}"

    # Verify both equal the expected CWD
    assert result_no_args == expected_cwd, f"Expected {expected_cwd}, got {result_no_args}"
    assert result_none_args == expected_cwd, f"Expected {expected_cwd}, got {result_none_args}"

    # Verify both are Path instances
    assert isinstance(result_no_args, Path), f"Expected Path, got {type(result_no_args)}"
    assert isinstance(result_none_args, Path), f"Expected Path, got {type(result_none_args)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
