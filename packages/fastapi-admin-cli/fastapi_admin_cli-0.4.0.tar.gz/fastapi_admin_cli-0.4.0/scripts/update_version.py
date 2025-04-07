#!/usr/bin/env python
"""
Update version numbers across the FastAPI Admin CLI project.
This script ensures that the version number is consistent in all locations.
"""
import os
import re
import sys
import toml
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.resolve()


def get_version_from_pyproject():
    """Read the version from pyproject.toml"""
    pyproject_path = ROOT_DIR / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"Error: pyproject.toml not found at {pyproject_path}")
        sys.exit(1)

    try:
        pyproject_data = toml.load(pyproject_path)
        version = pyproject_data["project"]["version"]
        return version
    except Exception as e:
        print(f"Error reading version from pyproject.toml: {e}")
        sys.exit(1)


def update_version_file(version):
    """Update the version in _version.py"""
    version_file = ROOT_DIR / "fastapi_admin" / "_version.py"

    content = f'''"""
Version information for FastAPI Admin CLI.
This file is auto-generated. Do not edit manually.
"""

__version__ = "{version}"
'''

    # Create the file if it doesn't exist
    version_file.parent.mkdir(parents=True, exist_ok=True)

    with open(version_file, "w") as f:
        f.write(content)

    print(f"Updated version in {version_file} to {version}")


def update_version(new_version=None):
    """
    Update all version numbers in the project.

    Args:
        new_version: If provided, update pyproject.toml to this version.
                     If None, use the existing version in pyproject.toml.
    """
    # Update pyproject.toml if a new version is specified
    if new_version:
        pyproject_path = ROOT_DIR / "pyproject.toml"
        try:
            pyproject_data = toml.load(pyproject_path)
            pyproject_data["project"]["version"] = new_version

            with open(pyproject_path, "w") as f:
                toml.dump(pyproject_data, f)

            print(f"Updated version in pyproject.toml to {new_version}")
        except Exception as e:
            print(f"Error updating version in pyproject.toml: {e}")
            sys.exit(1)

    # Get the current version from pyproject.toml
    version = get_version_from_pyproject()

    # Update the version in _version.py
    update_version_file(version)

    print(f"Version update complete: {version}")
    return version


def check_versions_match():
    """Check if versions in all files match"""
    pyproject_version = get_version_from_pyproject()

    # Check _version.py
    version_file = ROOT_DIR / "fastapi_admin" / "_version.py"
    if not version_file.exists():
        print(f"Warning: {version_file} does not exist")
        return False

    with open(version_file, "r") as f:
        content = f.read()
        version_match = re.search(
            r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if not version_match:
            print(f"Warning: Could not find __version__ in {version_file}")
            return False

        version_py = version_match.group(1)
        if version_py != pyproject_version:
            print(
                f"Version mismatch: pyproject.toml={pyproject_version}, _version.py={version_py}")
            return False

    print(f"All versions match: {pyproject_version}")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Update version numbers across the project")
    parser.add_argument("--new-version", help="Specify a new version number")
    parser.add_argument("--check", action="store_true",
                        help="Check if versions match")

    args = parser.parse_args()

    if args.check:
        if not check_versions_match():
            print("Versions do not match. Run without --check to update them.")
            sys.exit(1)
    else:
        update_version(args.new_version)
