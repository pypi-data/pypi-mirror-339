"""
Server commands for running the development server.
"""
import os
import typer
import importlib
import uvicorn
from pathlib import Path
from typing import Optional

from fastapi_admin.utils.file_utils import is_fastapi_project

app = typer.Typer(help="Run the development server")


@app.callback(invoke_without_command=True)
def main(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    reload: bool = typer.Option(True, help="Enable auto-reload"),
):
    """Run the development server using uvicorn."""
    # Check if current directory is a FastAPI project
    if not is_fastapi_project():
        typer.echo("Error: This command must be run from the root of a FastAPI project.")
        raise typer.Exit(1)
    
    typer.echo(f"Running server on http://{host}:{port}...")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
    )
