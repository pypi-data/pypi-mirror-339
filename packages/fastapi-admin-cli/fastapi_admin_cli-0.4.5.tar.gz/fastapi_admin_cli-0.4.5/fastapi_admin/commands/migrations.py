"""
Migration commands for database management.
"""
import typer
import subprocess
from typing import List, Optional

from fastapi_admin.utils.file_utils import is_fastapi_project

make_app = typer.Typer(help="Create new migration files")
migrate_app = typer.Typer(help="Apply migrations to the database")


@make_app.callback(invoke_without_command=True)
def make_migrations(
    message: str = typer.Option("", help="Migration message"),
    app_names: Optional[List[str]] = typer.Argument(
        None, help="Apps to make migrations for"),
):
    """Create new migration files using Alembic."""
    # Check if current directory is a FastAPI project
    if not is_fastapi_project():
        typer.echo(
            "Error: This command must be run from the root of a FastAPI project.")
        raise typer.Exit(1)

    # Ensure alembic is installed
    try:
        import alembic
    except ImportError:
        typer.echo(
            "Error: Alembic is not installed. Install it with: pip install alembic")
        raise typer.Exit(1)

    cmd = ["alembic", "revision", "--autogenerate"]
    if message:
        cmd.extend(["-m", message])

    # Run alembic command
    typer.echo("Creating migrations...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        typer.echo("Migrations created successfully!")
    else:
        typer.echo("Error creating migrations.")
        raise typer.Exit(1)


@migrate_app.callback(invoke_without_command=True)
def migrate(
    revision: str = typer.Option("head", help="Revision to migrate to"),
):
    """Apply migrations using Alembic."""
    # Check if current directory is a FastAPI project
    if not is_fastapi_project():
        typer.echo(
            "Error: This command must be run from the root of a FastAPI project.")
        raise typer.Exit(1)

    # Ensure alembic is installed
    try:
        import alembic
    except ImportError:
        typer.echo(
            "Error: Alembic is not installed. Install it with: pip install alembic")
        raise typer.Exit(1)

    cmd = ["alembic", "upgrade", revision]

    # Run alembic command
    typer.echo(f"Applying migrations to {revision}...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        typer.echo("Migrations applied successfully!")
    else:
        typer.echo("Error applying migrations.")
        raise typer.Exit(1)
