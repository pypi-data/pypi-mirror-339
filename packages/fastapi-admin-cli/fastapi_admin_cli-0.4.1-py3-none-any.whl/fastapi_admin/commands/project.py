"""
Project creation commands.
"""
import os
import shutil
import typer
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi_admin.utils.template_utils import render_template_directory
from fastapi_admin.utils.file_utils import create_directory

app = typer.Typer(help="Create a new FastAPI project")


@app.callback(invoke_without_command=True)
def main(
    project_name: str = typer.Argument(...,
                                       help="Name of the project to create"),
    directory: Optional[Path] = typer.Option(
        None, help="Directory where the project should be created"
    ),
    description: str = typer.Option(
        "A FastAPI project with admin dashboard", help="Project description"
    ),
    skip_git: bool = typer.Option(False, help="Skip git initialization"),
):
    """Create a new FastAPI project with a modular structure."""
    if directory is None:
        directory = Path.cwd() / project_name
    else:
        directory = directory / project_name

    typer.echo(f"Creating FastAPI project '{project_name}' in {directory}...")

    # Create project directory
    create_directory(directory)

    # Get template directory path - using an absolute path to the templates
    template_dir = Path(__file__).parent.parent / \
        "templates" / "project_template"

    if not template_dir.exists():
        typer.echo(f"Error: Template directory not found at {template_dir}")
        raise typer.Exit(1)

    # Context variables for templates
    context = {
        "project_name": project_name,
        "project_description": description,
    }

    # Copy and render template files
    render_template_directory(
        template_dir,
        directory,
        context=context
    )

    # Initialize git repository
    if not skip_git:
        try:
            cwd = os.getcwd()
            os.chdir(directory)
            os.system("git init")
            os.system("git add .")
            os.system('git commit -m "Initial commit from fastapi-admin"')
            os.chdir(cwd)  # Return to original directory
            typer.echo("Git repository initialized successfully")
        except Exception as e:
            typer.echo(
                f"Warning: Failed to initialize git repository: {str(e)}")

    typer.echo(f"Project '{project_name}' created successfully!")
    typer.echo(f"To run your project:")
    typer.echo(f"  cd {project_name}")
    typer.echo(f"  pip install -e .")
    typer.echo(f"  uvicorn app.main:app --reload")
