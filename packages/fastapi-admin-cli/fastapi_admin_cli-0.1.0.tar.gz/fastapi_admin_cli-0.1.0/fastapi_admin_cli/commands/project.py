import typer
import uvicorn
from pathlib import Path
import importlib
import subprocess
from typing import List, Optional
from .registry import registry

project_commands = typer.Typer()

@project_commands.command("runserver")
def runserver(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind the server to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind the server to"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable auto-reload on file changes"),
):
    """Run the development server."""
    typer.echo(f"Starting development server at http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)

@project_commands.command("makemigrations")
def makemigrations(
    name: str = typer.Option(None, "--name", "-n", help="Name of the migration"),
    args: Optional[List[str]] = typer.Argument(None, help="Arguments to pass to alembic"),
):
    """Create new migration files based on the changes detected in the models."""
    cmd = ["alembic", "revision", "--autogenerate"]
    
    if name:
        cmd.extend(["-m", name])
    
    if args:
        cmd.extend(args)
    
    typer.echo(f"Creating migrations with command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

@project_commands.command("migrate")
def migrate(
    revision: str = typer.Option("head", "--revision", "-r", help="Revision to upgrade to"),
    args: Optional[List[str]] = typer.Argument(None, help="Arguments to pass to alembic"),
):
    """Apply migrations to the database."""
    cmd = ["alembic", "upgrade", revision]
    
    if args:
        cmd.extend(args)
    
    typer.echo(f"Applying migrations with command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

@project_commands.command("startapp")
def startapp(
    app_name: str = typer.Argument(..., help="Name of the app to create"),
):
    """Create a new app within the project."""
    from fastapi_admin_cli.commands.startapp import create_new_app
    try:
        create_new_app(app_name)
        typer.echo(f"\n✅ App '{app_name}' created successfully!")
    except Exception as e:
        typer.echo(f"Error creating app: {str(e)}", err=True)
        raise typer.Exit(1)

@project_commands.command("dbshell")
def dbshell():
    """Launch an interactive PostgreSQL shell in the database container."""
    compose_dir = Path.cwd() / "docker" / "compose"
    env_file = Path.cwd() / ".env"
    
    if not compose_dir.exists():
        typer.echo("Error: docker/compose directory not found", err=True)
        raise typer.Exit(1)
        
    cmd = [
        "docker", "compose",
        "-f", "docker-compose.yml",
        "exec", "postgres",
        "psql", "-U", "postgres"
    ]
    
    typer.echo("Launching PostgreSQL shell...")
    try:
        subprocess.run(cmd, cwd=compose_dir, check=True)
    except subprocess.CalledProcessError:
        typer.echo("Failed to launch dbshell. Make sure the database container is running.", err=True)
        raise typer.Exit(1)
    except KeyboardInterrupt:
        typer.echo("\nExited dbshell.")

@project_commands.command("appshell")
def appshell():
    """Launch a shell in the FastAPI application container."""
    compose_dir = Path.cwd() / "docker" / "compose"
    
    if not compose_dir.exists():
        typer.echo("Error: docker/compose directory not found", err=True)
        raise typer.Exit(1)
        
    cmd = [
        "docker", "compose",
        "-f", "docker-compose.yml",
        "exec", "api", "bash"
    ]
    
    typer.echo("Launching application container shell...")
    try:
        subprocess.run(cmd, cwd=compose_dir, check=True)
    except subprocess.CalledProcessError:
        typer.echo("Failed to launch appshell. Make sure the application container is running.", err=True)
        raise typer.Exit(1)
    except KeyboardInterrupt:
        typer.echo("\nExited appshell.")

# Register project commands
registry.register("project", project_commands)

