"""
Command to create a new FastAPI project.
"""
import os
import re
import sys
import logging
from pathlib import Path
from typing import Optional
import typer

from fastapi_admin.utils.template_utils import render_templates
from fastapi_admin.utils.file_utils import create_directory

logger = logging.getLogger(__name__)

app = typer.Typer(help="Create a new FastAPI project.")


def ensure_template_directory_exists():
    """
    Ensure the project template directory exists with necessary files.
    """
    template_dir = Path(__file__).parent.parent / \
        "templates" / "project_template"
    app_dir = template_dir / "app"

    # If template directory doesn't exist or is empty, create a basic structure
    if not template_dir.exists() or not any(template_dir.iterdir()):
        logger.warning(
            "Template directory does not exist or is empty. Creating basic template structure.")
        try:
            # Create directories
            template_dir.mkdir(parents=True, exist_ok=True)
            app_dir.mkdir(exist_ok=True)

            # Create basic main.py template
            main_py_path = app_dir / "main.py.tpl"
            with open(main_py_path, "w") as f:
                f.write('''"""
Main FastAPI application module.
"""
from fastapi import FastAPI

app = FastAPI(
    title="${project_name}",
    description="${project_name} API",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to ${project_name}"}
''')
            logger.info(f"Created template: {main_py_path}")

            # Create basic pyproject.toml template
            pyproject_path = template_dir / "pyproject.toml.tpl"
            with open(pyproject_path, "w") as f:
                f.write('''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "${project_name}"
version = "0.1.0"
description = "FastAPI project created with fastapi-admin-cli"
requires-python = ">=3.8"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.15.0",
]
''')
            logger.info(f"Created template: {pyproject_path}")

            return True
        except Exception as e:
            logger.error(f"Failed to create template structure: {str(e)}")
            return False

    # Check if app/main.py template exists, create if not
    if not (app_dir / "main.py.tpl").exists() and not (app_dir / "main.py").exists():
        try:
            app_dir.mkdir(exist_ok=True)
            main_py_path = app_dir / "main.py.tpl"
            with open(main_py_path, "w") as f:
                f.write('''"""
Main FastAPI application module.
"""
from fastapi import FastAPI

app = FastAPI(
    title="${project_name}",
    description="${project_name} API",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to ${project_name}"}
''')
            logger.info(f"Created missing template: {main_py_path}")
        except Exception as e:
            logger.error(f"Failed to create main.py template: {str(e)}")
            return False

    return True


@app.callback(invoke_without_command=True)
def main(
    project_name: str = typer.Argument(...,
                                       help="Name of the project to create."),
    directory: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Directory where the project will be created."
    ),
):
    """
    Create a new FastAPI project with the specified name.
    """
    # Validate project name
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', project_name):
        logger.error(
            "Project name must start with a letter and contain only letters, numbers, and underscores."
        )
        sys.exit(1)

    # Determine the project directory
    if directory:
        project_dir = Path(directory) / project_name
    else:
        project_dir = Path.cwd() / project_name

    # Create the project directory
    try:
        create_directory(project_dir)
    except Exception as e:
        logger.error(f"Failed to create project directory: {str(e)}")
        sys.exit(1)

    print(f"Creating FastAPI project '{project_name}' in {project_dir}...")

    # Get the template directory
    template_dir = Path(__file__).parent.parent / \
        "templates" / "project_template"

    # Ensure template directory exists with necessary files
    if not ensure_template_directory_exists():
        logger.error(
            "Failed to ensure template directory exists with necessary files.")
        sys.exit(1)

    # Define the context for template rendering
    context = {
        "project_name": project_name,
    }

    # Render the project templates
    try:
        render_templates(template_dir, project_dir, context)
        print(f"\nProject '{project_name}' created successfully!")
        print(f"\nTo get started:")
        print(f"  cd {project_name}")
        print(f"  python -m venv .venv")
        print(f"  source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
        print(f"  pip install -e .")
        print(f"  fastapi-admin runserver")
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        logger.debug("Detailed error:", exc_info=True)
        sys.exit(1)
