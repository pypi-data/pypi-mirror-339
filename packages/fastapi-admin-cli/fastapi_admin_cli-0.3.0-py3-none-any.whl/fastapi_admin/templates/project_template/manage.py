#!/usr/bin/env python
"""
Management script for the FastAPI Admin CLI.
"""
import os
import sys
import argparse
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, cwd=None):
    """Run a shell command and log output."""
    logger.info(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            text=True, 
            cwd=cwd,
            capture_output=True
        )
        if result.stdout:
            logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with error code {e.returncode}")
        if e.stdout:
            logger.info(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False

def run_server(args):
    """Run the development server."""
    port = args.port
    host = args.host
    reload = "--reload" if args.reload else ""
    command = f"uvicorn app.main:app --host {host} --port {port} {reload}"
    run_command(command)

def create_app(args):
    """Create a new app module."""
    app_name = args.name.lower()
    if not app_name.isidentifier():
        logger.error(f"App name '{app_name}' is not a valid Python identifier.")
        return
    
    # Determine app directory
    app_dir = Path("app") / app_name
    if app_dir.exists():
        logger.error(f"App directory '{app_dir}' already exists.")
        return
    
    # Create app directory
    app_dir.mkdir(parents=True)
    
    # Create files from template
    template_dir = Path("templates") / "app_template"
    
    # Get model name (capitalized)
    model_name = "".join(word.capitalize() for word in app_name.split("_"))
    model_name_plural = f"{model_name}s"
    table_name = app_name
    model_description = f"{model_name} model"
    
    # Process all template files
    for template_file in template_dir.glob("*.py"):
        target_file = app_dir / template_file.name
        
        with open(template_file, "r") as f:
            content = f.read()
        
        # Replace placeholders
        content = content.replace("{{ model_name }}", model_name)
        content = content.replace("{{ model_name_plural }}", model_name_plural)
        content = content.replace("{{ table_name }}", table_name)
        content = content.replace("{{ model_description }}", model_description)
        
        with open(target_file, "w") as f:
            f.write(content)
    
    # Create __init__.py
    with open(app_dir / "__init__.py", "w") as f:
        f.write(f"""# Import commonly used components for easier imports elsewhere
from .models import {model_name}
from .schemas import {model_name}Read, {model_name}Create, {model_name}Update
from .services import {model_name}Service
from .routes import router as {app_name}_router
""")
    
    logger.info(f"Created app '{app_name}' at {app_dir}")
    logger.info(f"Remember to add your new app to app/core/main_routes.py and app/core/main_models.py")

def run_migrations(args):
    """Run database migrations."""
    if args.command == 'create':
        message = args.message if args.message else "Migration"
        command = f"alembic revision --autogenerate -m \"{message}\""
    elif args.command == 'upgrade':
        target = args.revision if args.revision else "head"
        command = f"alembic upgrade {target}"
    elif args.command == 'downgrade':
        target = args.revision if args.revision else "-1"
        command = f"alembic downgrade {target}"
    elif args.command == 'history':
        command = "alembic history"
    else:
        logger.error(f"Unknown migration command: {args.command}")
        return
    
    run_command(command)

def main():
    """Run administrative tasks."""
    # Add the project root to the Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    try:
        from fastapi_admin.cli import run_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import fastapi-admin. Make sure it's installed and "
            "available on your PYTHONPATH environment variable."
        ) from exc
    
    run_from_command_line()

if __name__ == "__main__":
    main()
