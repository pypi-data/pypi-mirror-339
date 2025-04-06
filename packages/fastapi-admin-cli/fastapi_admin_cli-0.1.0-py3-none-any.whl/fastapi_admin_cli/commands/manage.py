import os
import sys
import subprocess
from pathlib import Path
import typer

def find_manage_py() -> Path:
    """
    Find the manage.py file by traversing up from the current directory.
    
    Returns:
        Path to manage.py or None if not found
    """
    current_dir = Path.cwd()
    
    # First, check the current directory
    manage_py = current_dir / "manage.py"
    if manage_py.exists():
        return manage_py
    
    # If not found, traverse up to 3 levels
    for _ in range(3):
        current_dir = current_dir.parent
        manage_py = current_dir / "manage.py"
        if manage_py.exists():
            return manage_py
    
    return None

def run_manage_command(manage_py: Path, command: str, args: list[str]) -> None:
    """
    Run a command using the project's manage.py script.
    
    Args:
        manage_py: Path to the manage.py file
        command: The command to run
        args: Additional arguments to pass to the command
    """
    if command == "runserver":
        # For runserver, we'll use uvicorn directly
        cmd = [sys.executable, str(manage_py), "runserver"] + args
    elif command in ["makemigrations", "migrate"]:
        # For migration commands, use our wrappers
        cmd = [sys.executable, str(manage_py), command] + args
    else:
        # For all other commands, pass directly to alembic
        cmd = [sys.executable, str(manage_py), command] + args
    
    try:
        result = subprocess.run(cmd)
        if result.returncode != 0:
            typer.echo(f"Command failed with exit code {result.returncode}", err=True)
            raise typer.Exit(result.returncode)
    except KeyboardInterrupt:
        typer.echo("\nCommand interrupted by user.")
        raise typer.Exit(1)
