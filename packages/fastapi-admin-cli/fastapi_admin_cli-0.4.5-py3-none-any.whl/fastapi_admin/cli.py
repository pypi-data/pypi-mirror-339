"""
Command-line interface for FastAPI Admin.
"""
import logging
import sys
import typer
from typing import Optional

from fastapi_admin.commands import project, app
from fastapi_admin._version import __version__
from fastapi_admin.utils.git_utils import clone_or_update_templates, DEFAULT_TEMPLATE_REPO_URL, DEFAULT_TEMPLATE_DIR

# Create the app
cli = typer.Typer(
    name="fastapi-admin",
    help="Django-like CLI tool for FastAPI applications.",
    add_completion=False,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)
logger = logging.getLogger("fastapi_admin.cli")

# Register commands
cli.add_typer(project.app, name="startproject")
cli.add_typer(app.app, name="startapp")

# Add debug option to the CLI
debug_option = typer.Option(
    False, "--debug", help="Enable debug mode with detailed error messages."
)


@cli.command("update-templates")
def update_templates():
    """Update or download template files from the repository."""
    try:
        if clone_or_update_templates():
            typer.echo(
                f"Templates updated successfully at {DEFAULT_TEMPLATE_DIR}")
            typer.echo(f"Template repository: {DEFAULT_TEMPLATE_REPO_URL}")
        else:
            typer.echo("Failed to update templates. Check logs for details.")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error updating templates: {str(e)}")
        raise typer.Exit(1)


@cli.callback()
def callback(debug: bool = debug_option):
    """Set up CLI options."""
    if debug:
        # Set logging level to DEBUG if debug option is enabled
        logging.getLogger("fastapi_admin").setLevel(logging.DEBUG)


def run_from_command_line():
    """
    Entry point for the command-line interface.
    This function is called when the fastapi-admin command is run.
    """
    try:
        cli()
    except Exception as e:
        if "--debug" in sys.argv:
            # Show full traceback in debug mode
            logger.exception("An error occurred:")
        else:
            # Show simplified error message in normal mode
            logger.error(f"Error: {str(e)}")
            logger.error(
                "Run with --debug for more detailed error information")
        sys.exit(1)


if __name__ == "__main__":
    run_from_command_line()
