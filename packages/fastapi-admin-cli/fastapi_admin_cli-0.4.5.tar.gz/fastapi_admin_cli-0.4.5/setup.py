#!/usr/bin/env python
"""
Setup script for fastapi-admin-cli.
This script is mainly for development installation.
"""
import os
import sys
import toml
from setuptools import setup

# Get the project directory
project_dir = os.path.abspath(os.path.dirname(__file__))

# Load the pyproject.toml to get package info
pyproject_path = os.path.join(project_dir, "pyproject.toml")
pyproject_data = toml.load(pyproject_path)

# Extract the package metadata
package_info = pyproject_data.get("project", {})
package_name = package_info.get("name", "fastapi-admin-cli")
version = package_info.get("version", "0.0.0")
description = package_info.get("description", "")

# Package dependencies
dependencies = package_info.get("dependencies", [])
optional_deps = package_info.get("optional-dependencies", {})

# Setup configuration
setup(
    name=package_name,
    version=version,
    description=description,
    python_requires=">=3.8",
    packages=["fastapi_admin", "fastapi_admin.commands",
              "fastapi_admin.utils", "scripts"],
    install_requires=dependencies,
    extras_require=optional_deps,
    entry_points={
        "console_scripts": [
            "fastapi-admin=fastapi_admin.cli:run_from_command_line",
            "create-template-structure=scripts.create_template_structure:create_template_structure",
        ],
    },
)
