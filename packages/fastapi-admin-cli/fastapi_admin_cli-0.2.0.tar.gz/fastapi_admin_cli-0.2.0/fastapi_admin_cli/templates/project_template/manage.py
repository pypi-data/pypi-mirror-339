#!/usr/bin/env python
import sys
from pathlib import Path
import typer
from fastapi_admin_cli.commands.registry import registry
from fastapi_admin_cli.commands import project  # This import registers the commands

def main():
    """{{ project_name }} management script."""
    # Add the project directory to sys.path
    project_dir = Path(__file__).parent.absolute()
    sys.path.insert(0, str(project_dir))

    # Create a new Typer app for the project
    app = typer.Typer(
        name="{{ project_name }}",
        help="{{ project_name }} management script",
        add_completion=False,
    )

    # Get project commands from the registry
    project_commands = registry.get_command("project")
    if project_commands:
        app.add_typer(project_commands, name="")

    app()

if __name__ == "__main__":
    main()
