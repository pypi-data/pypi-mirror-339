import os
import sys
import typer
from pathlib import Path
from typing import Optional
import subprocess

from fastapi_admin_cli.commands.startproject import create_new_project
from fastapi_admin_cli.commands.startapp import create_new_app
from fastapi_admin_cli.commands.manage import find_manage_py, run_manage_command

app = typer.Typer(
    name="fastapi-admin",
    help="A CLI tool for FastAPI project management inspired by Django's admin",
    add_completion=False,
)

@app.command("startproject")
def startproject(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
    directory: Optional[Path] = typer.Option(
        None, "--directory", "-d", help="Directory to create the project in"
    ),
):
    """
    Create a new FastAPI project with the specified name.
    """
    typer.echo(f"Creating new FastAPI project: {project_name}")
    create_new_project(project_name, directory)
    typer.echo(f"\n✅ Project '{project_name}' created successfully!")
    typer.echo(f"To start your development server, run:")
    typer.echo(f"  cd {project_name}")
    typer.echo(f"  python manage.py runserver")

@app.command("startapp")
def startapp(
    app_name: str = typer.Argument(..., help="Name of the app to create"),
):
    """
    Create a new app within an existing FastAPI project.
    This must be run from within a FastAPI project.
    """
    typer.echo(f"Creating new app: {app_name}")
    try:
        create_new_app(app_name)
        typer.echo(f"\n✅ App '{app_name}' created successfully!")
    except Exception as e:
        typer.echo(f"Error creating app: {str(e)}", err=True)
        raise typer.Exit(1)

@app.command("manage")
def manage(
    command: str = typer.Argument(..., help="The manage.py command to run"),
    args: Optional[list[str]] = typer.Argument(None, help="Arguments to pass to the command"),
):
    """
    Run a command using the project's manage.py script.
    This is a pass-through to the project's manage.py.
    """
    manage_py = find_manage_py()
    if not manage_py:
        typer.echo("Error: manage.py not found. Make sure you're in a FastAPI project directory.", err=True)
        raise typer.Exit(1)
    
    run_manage_command(manage_py, command, args or [])

if __name__ == "__main__":
    app()
