"""
Command to create a new FastAPI project.
"""
import re
import sys
import logging
from pathlib import Path
from typing import Optional
import typer

from fastapi_admin.utils.template_utils import render_templates
from fastapi_admin.utils.file_utils import create_directory
from fastapi_admin.utils.git_utils import clone_or_update_templates, get_template_dir

logger = logging.getLogger(__name__)

app = typer.Typer(help="Create a new FastAPI project.")


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
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', project_name):
        logger.error(
            "Project name must start with a letter and contain only letters, numbers, and underscores."
        )
        sys.exit(1)

    if directory:
        project_dir = Path(directory) / project_name
    else:
        project_dir = Path.cwd() / project_name

    try:
        create_directory(project_dir)
    except Exception as e:
        logger.error(f"Failed to create project directory: {str(e)}")
        sys.exit(1)

    print(f"Creating FastAPI project '{project_name}' in {project_dir}...")

    if not clone_or_update_templates():
        logger.error("Failed to obtain templates from repository.")
        sys.exit(1)

    template_dir = get_template_dir("project_template")

    if not template_dir.exists() or not any(template_dir.iterdir()):
        logger.error(
            f"Project template directory not found in repository: {template_dir}")
        sys.exit(1)

    context = {
        "project_name": project_name,
        "project_description": f"FastAPI project created with fastapi-admin-cli"
    }

    exclude_patterns = [
        '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.DS_Store',
        '*.so', '*.dylib', '.git', '.gitignore~', '*.swp'
    ]

    try:
        render_templates(template_dir, project_dir,
                         context, exclude=exclude_patterns)
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
