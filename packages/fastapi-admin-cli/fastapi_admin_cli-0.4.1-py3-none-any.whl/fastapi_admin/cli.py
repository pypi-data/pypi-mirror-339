"""
Main CLI entry point for the FastAPI Admin CLI.
"""
import os
import sys
import typer
from typing import Optional
from pathlib import Path
import logging
import traceback

# Import commands with renamed imports to avoid name conflict
from fastapi_admin.commands import project as project_cmd
from fastapi_admin.commands import app as app_cmd
from fastapi_admin.commands import server as server_cmd
from fastapi_admin.commands import migrations
from fastapi_admin._version import __version__

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


@app.callback()
def common(
    version: bool = typer.Option(
        False, "--version", help="Show version information and exit"),
    debug: bool = typer.Option(
        False, "--debug", help="Enable debug mode with detailed error messages"),
):
    """
    FastAPI Admin CLI - A Django-inspired CLI tool for FastAPI applications
    """
    if version:
        typer.echo(f"FastAPI Admin CLI version: {__version__}")
        raise typer.Exit()

    # Set debug logging if requested
    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s: %(message)s")
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")


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
        if "--debug" in sys.argv:
            logger.error(f"Error: {str(e)}")
            logger.error(traceback.format_exc())
        else:
            logger.error(f"Error: {str(e)}")
            logger.error(
                "Run with --debug for more detailed error information")
        sys.exit(1)


if __name__ == "__main__":
    run_from_command_line()
