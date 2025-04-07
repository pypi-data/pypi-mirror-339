"""
Main CLI entry point for the FastAPI Admin CLI.
"""
import os
import sys
import typer
from typing import Optional
from pathlib import Path
import logging

# Import commands with renamed imports to avoid name conflict
from fastapi_admin.commands import project as project_cmd
from fastapi_admin.commands import app as app_cmd
from fastapi_admin.commands import server as server_cmd
from fastapi_admin.commands import migrations

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = typer.Typer(
    name="fastapi-admin",
    help="Django-inspired CLI for FastAPI applications",
    add_completion=False,
)

# Register command modules
app.add_typer(project_cmd.app, name="startproject")
app.add_typer(app_cmd.app, name="startapp")
app.add_typer(server_cmd.app, name="runserver")
app.add_typer(migrations.make_app, name="makemigrations")
app.add_typer(migrations.migrate_app, name="migrate")


def run_from_command_line():
    """
    Entry point for the CLI when executed directly.
    """
    try:
        # Handle case when running from within a project
        cwd = Path.cwd()
        if (cwd / "manage.py").exists():
            sys.path.insert(0, str(cwd))
        
        app()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_from_command_line()
