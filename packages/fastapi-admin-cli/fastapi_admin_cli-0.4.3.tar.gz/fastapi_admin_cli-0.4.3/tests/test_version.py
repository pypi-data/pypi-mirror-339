"""
Tests to ensure that version numbers are consistent across the package.
"""
import os
import re
import toml


def get_version_from_pyproject():
    """Get the version from pyproject.toml"""
    pyproject_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "pyproject.toml")
    with open(pyproject_path, "r") as f:
        data = toml.loads(f.read())
        return data["project"]["version"]


def get_version_from_init():
    """Get the version from __init__.py"""
    from fastapi_admin import __version__
    return __version__


def test_versions_match():
    """Test that the version numbers match in all locations"""
    pyproject_version = get_version_from_pyproject()
    init_version = get_version_from_init()

    assert pyproject_version == init_version, \
        f"Version mismatch: pyproject.toml={pyproject_version}, __init__.py={init_version}"

    # Ensure the version follows semantic versioning (e.g., 1.2.3)
    assert re.match(r'^\d+\.\d+\.\d+$', init_version), \
        f"Version {init_version} does not follow semantic versioning (X.Y.Z)"
