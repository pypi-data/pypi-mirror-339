"""
App management commands.
"""
import os
import typer
import re
from pathlib import Path
import shutil
import logging

from fastapi_admin.utils.template_utils import render_template_directory
from fastapi_admin.utils.file_utils import create_directory, is_fastapi_project

# Configure logging
logger = logging.getLogger(__name__)

app = typer.Typer(help="Create a new app within a FastAPI project")


@app.callback(invoke_without_command=True)
def main(
    app_name: str = typer.Argument(..., help="Name of the app to create"),
):
    """Create a new app module within an existing FastAPI project."""
    # Check if current directory is a FastAPI project
    if not is_fastapi_project():
        typer.echo(
            "Error: This command must be run from the root of a FastAPI project.")
        raise typer.Exit(1)

    # Validate app name
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', app_name):
        typer.echo(
            f"Error: App name '{app_name}' must start with a letter and contain only letters, numbers, and underscores.")
        raise typer.Exit(1)

    # Create app directory
    app_dir = Path.cwd() / "app" / app_name.lower()
    if app_dir.exists():
        typer.echo(f"Error: App '{app_name}' already exists at {app_dir}.")
        raise typer.Exit(1)

    typer.echo(f"Creating app '{app_name}' in {app_dir}...")

    try:
        # Create app directory
        create_directory(app_dir)

        # Get template directory
        template_dir = Path(__file__).parent.parent / \
            "templates" / "app_template"

        if not template_dir.exists():
            typer.echo(
                f"Error: Template directory not found at {template_dir}")
            raise typer.Exit(1)

        # Generate model name (capitalized)
        model_name = "".join(word.capitalize() for word in app_name.split("_"))
        model_name_plural = f"{model_name}s"
        table_name = app_name.lower()

        # Context variables for templates
        context = {
            "app_name": app_name,
            "app_name_lowercase": app_name.lower(),
            "model_name": model_name,
            "model_name_plural": model_name_plural,
            "table_name": table_name,
            "model_description": f"{model_name} model",
        }

        # Copy and render template files
        render_template_directory(
            template_dir,
            app_dir,
            context=context
        )

        # Create __init__.py with imports
        with open(app_dir / "__init__.py", "w") as f:
            f.write(f"""# Import commonly used components for easier imports elsewhere
                        from .models import *
                        from .schemas import *
                        from .services import *
                        from .routes import router as {app_name}_router
                        """
                    )

        # Update main_routes.py to include the new app
        update_main_routes(app_name)

        # Update main_models.py to import the model
        update_main_models(app_name, model_name)

        typer.echo(f"✅ App '{app_name}' created successfully!")
        typer.echo(
            f"📝 Remember to add your app to app/core/main_routes.py if it wasn't automatically added")
        typer.echo(
            f"📝 Remember to add your model to app/core/main_models.py if it wasn't automatically added")

    except Exception as e:
        # If anything fails, clean up the created directory
        if app_dir.exists():
            shutil.rmtree(app_dir)
        typer.echo(f"Error creating app: {str(e)}")
        logger.exception("Exception during app creation:")
        raise typer.Exit(1)


def update_main_routes(app_name: str):
    """Update main_routes.py to import the new app's routes."""
    routes_file = Path.cwd() / "app" / "core" / "main_routes.py"
    if not routes_file.exists():
        typer.echo(
            "Warning: main_routes.py not found. Skipping automatic route inclusion.")
        return

    try:
        with open(routes_file, "r") as f:
            content = f.read()

        app_name_lower = app_name.lower()
        import_line = f"from app.{app_name_lower}.routes import router as {app_name_lower}_router"
        include_line = f"main_router.include_router(\n    {app_name_lower}_router,\n    prefix=f\"/api/{{api_version}}/{app_name_lower}\",\n    tags=[\"{app_name}\"])"

        # Check if import already exists
        if import_line not in content:
            # Find the import section
            import_section_end = 0
            lines = content.split("\n")

            # Find where the imports end
            for i, line in enumerate(lines):
                if line.startswith("from") or line.startswith("import"):
                    import_section_end = i + 1
                elif line.strip() and import_section_end > 0 and not line.startswith("#"):
                    break

            # Insert the import
            lines.insert(import_section_end, import_line)

            # Find where to add router inclusion
            router_section = None
            for i, line in enumerate(lines):
                if "# Import and include your app-specific routers here" in line:
                    router_section = i
                    break

            if router_section:
                # Find the right place to insert after the comment
                for i in range(router_section, len(lines)):
                    if "# Example:" in lines[i]:
                        # Insert before the example
                        lines.insert(i, include_line)
                        lines.insert(i, "")
                        break
            else:
                # If comment not found, add at the end if main_router is defined
                if "main_router.include_router(" in content:
                    for i, line in enumerate(lines):
                        if "main_router.include_router(" in line and ")" in line:
                            lines.insert(i + 1, include_line)
                            break

            updated_content = "\n".join(lines)

            with open(routes_file, "w") as f:
                f.write(updated_content)

            typer.echo(
                f"Updated main_routes.py to include routes from '{app_name}'")
        else:
            typer.echo(
                f"Routes for '{app_name}' already included in main_routes.py")

    except Exception as e:
        typer.echo(f"Warning: Failed to update main_routes.py: {str(e)}")


def update_main_models(app_name: str, model_name: str):
    """Update main_models.py to import the app's model."""
    models_file = Path.cwd() / "app" / "core" / "main_models.py"
    if not models_file.exists():
        typer.echo(
            "Warning: main_models.py not found. Skipping automatic model import.")
        return

    try:
        with open(models_file, "r") as f:
            content = f.read()

        app_name_lower = app_name.lower()
        import_line = f"from app.{app_name_lower}.models import {model_name}"

        # Check if import already exists
        if import_line not in content:
            # Find the comment about importing app-specific models
            lines = content.split("\n")
            position = None

            for i, line in enumerate(lines):
                if "# Import your app-specific models here" in line or "# Example:" in line:
                    position = i
                    break

            if position:
                lines.insert(position, import_line)
            else:
                # If comment not found, add after the last import
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith("from "):
                        lines.insert(i + 1, "")
                        lines.insert(i + 2, "# App-specific models")
                        lines.insert(i + 3, import_line)
                        break

            updated_content = "\n".join(lines)

            with open(models_file, "w") as f:
                f.write(updated_content)

            typer.echo(
                f"Updated main_models.py to import the '{model_name}' model")
        else:
            typer.echo(
                f"Model '{model_name}' already imported in main_models.py")

    except Exception as e:
        typer.echo(f"Warning: Failed to update main_models.py: {str(e)}")
