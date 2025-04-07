"""
Command to create a new FastAPI application module.
"""
import re
import sys
import logging
from pathlib import Path
from typing import Optional
import typer

from fastapi_admin.utils.template_utils import render_template_directory
from fastapi_admin.utils.file_utils import create_directory
from fastapi_admin.utils.git_utils import clone_or_update_templates, get_template_dir

logger = logging.getLogger(__name__)

app = typer.Typer(help="Create a new FastAPI application module.")


@app.callback(invoke_without_command=True)
def main(
    app_name: str = typer.Argument(..., help="Name of the app to create"),
    directory: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Directory where the app will be created"
    ),
):
    """
    Create a new FastAPI application module with the specified name.
    """
    # Validate app name
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', app_name):
        logger.error(
            "App name must start with a letter and contain only letters, numbers, and underscores."
        )
        sys.exit(1)

    # Determine app directory
    if directory:
        app_dir = Path(directory) / app_name
    else:
        # First check if we're inside a project directory
        current_dir = Path.cwd()
        app_module_dir = current_dir / "app"

        if app_module_dir.exists() and app_module_dir.is_dir():
            # We're in the project root, create app in app/
            app_dir = app_module_dir / app_name
        else:
            # Check if we're already in the app directory
            parent_dir = current_dir.parent
            if parent_dir.name == "app" and parent_dir.exists():
                app_dir = parent_dir / app_name
            else:
                # Create in current directory
                app_dir = current_dir / app_name

    # Create app directory
    try:
        create_directory(app_dir)
    except Exception as e:
        logger.error(f"Failed to create app directory: {str(e)}")
        sys.exit(1)

    print(f"Creating app '{app_name}' in {app_dir}...")

    # Clone or update templates repository
    if not clone_or_update_templates():
        logger.error("Failed to obtain templates from repository.")
        sys.exit(1)

    # Get the template directory
    template_dir = get_template_dir("app_template")

    # Check if template directory exists
    if not template_dir.exists() or not any(template_dir.iterdir()):
        logger.error(
            f"App template directory not found in repository: {template_dir}")
        sys.exit(1)

    # Get model name (capitalized)
    model_name = "".join(word.capitalize() for word in app_name.split("_"))
    model_name_plural = f"{model_name}s"
    table_name = app_name
    model_description = f"{model_name} model"

    # Define context for template rendering
    context = {
        "app_name": app_name,
        "model_name": model_name,
        "model_name_plural": model_name_plural,
        "table_name": table_name,
        "model_description": model_description,
    }

    # Define exclusion patterns
    exclude_patterns = [
        '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.DS_Store',
        '*.so', '*.dylib', '.git', '.gitignore~', '*.swp'
    ]

    # Render templates
    try:
        render_template_directory(
            template_dir,
            app_dir,
            context=context,
            exclude=exclude_patterns
        )
        print(f"\nApp '{app_name}' created successfully in {app_dir}")
        print("\nRemember to:")
        print(f"1. Add your new app to app/core/main_routes.py:")
        print(f"   from app.{app_name}.routes import {app_name}_router")
        print(
            f"   main_router.include_router({app_name}_router, prefix=f\"/api/{{api_version}}/{app_name}\", tags=[\"{app_name}\"])")
        print(f"2. Add your model to app/core/main_models.py:")
        print(f"   from app.{app_name}.models import {model_name}")
    except Exception as e:
        logger.error(f"Exception during app creation: {e}")
        logger.debug("Detailed error:", exc_info=True)
        sys.exit(1)
