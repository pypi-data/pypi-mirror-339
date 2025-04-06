import os
from pathlib import Path
import typer
import shutil
from jinja2 import Environment, FileSystemLoader
import importlib.resources as pkg_resources

from fastapi_admin_cli.templates import app_template
from fastapi_admin_cli.commands.manage import find_manage_py

def create_new_app(app_name: str) -> None:
    """
    Create a new app within an existing FastAPI project.
    
    Args:
        app_name: Name of the app to create
    """
    # Ensure we're in a FastAPI project
    manage_py = find_manage_py()
    if not manage_py:
        typer.echo("Error: manage.py not found. Make sure you're in a FastAPI project directory.", err=True)
        raise typer.Exit(1)
    
    project_root = manage_py.parent
    app_dir = project_root / "app" / app_name
    
    if app_dir.exists():
        typer.echo(f"App '{app_name}' already exists at {app_dir}.", err=True)
        raise typer.Exit(1)
    
    # Create app directory
    app_dir.mkdir(parents=True, exist_ok=True)
    
    # Create templates environment
    template_dir = pkg_resources.files(app_template)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    
    # Context for template rendering
    context = {
        "app_name": app_name,
        "app_class_name": "".join(word.capitalize() for word in app_name.split("_")),
    }
    
    # Process all template files
    _process_templates(env, context, template_dir, app_dir)
    
    # Update main_routes.py to include the new app's router
    _update_main_routes(project_root, app_name)
    
    # Update main_models.py to include the new app's models
    _update_main_models(project_root, app_name)
    
    typer.echo(f"Creating app structure:")
    _print_tree(app_dir, prefix="├── ")

def _process_templates(env, context, template_dir, output_dir):
    """Process all template files, rendering them with the context."""
    for item in template_dir.iterdir():
        if item.is_file():
            template = env.get_template(item.name)
            output_content = template.render(**context)
            
            output_file_path = output_dir / item.name.replace('__app_name__', context['app_name'])
            
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(output_content)

def _update_main_routes(project_root: Path, app_name: str) -> None:
    """Update the main_routes.py file to include the new app's router."""
    main_routes_path = project_root / "app" / "core" / "main_routes.py"
    
    if not main_routes_path.exists():
        typer.echo("Warning: Could not find main_routes.py to update. You'll need to manually add the new router.")
        return
    
    with open(main_routes_path, 'r') as f:
        lines = f.readlines()
    
    import_line = f"from app.{app_name}.routes import {app_name}_router\n"
    router_line = f"main_router.include_router({app_name}_router, prefix=f\"/api/{{version}}/{app_name}\", tags=[\"{app_name}\"])\n"
    
    # Check if import already exists
    if import_line not in lines:
        # Find the last import line
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('from') or line.startswith('import'):
                last_import_idx = i
        
        # Insert import after the last import
        lines.insert(last_import_idx + 1, import_line)
    
    # Check if router inclusion already exists
    if router_line not in lines:
        # Find the last router inclusion line
        last_router_idx = 0
        for i, line in enumerate(lines):
            if 'main_router.include_router' in line:
                last_router_idx = i
        
        # Insert router inclusion after the last one
        if last_router_idx > 0:
            lines.insert(last_router_idx + 1, router_line)
        else:
            # If no router inclusions found, add after the main_router definition
            for i, line in enumerate(lines):
                if 'main_router = APIRouter()' in line:
                    lines.insert(i + 2, router_line)
                    break
    
    with open(main_routes_path, 'w') as f:
        f.writelines(lines)

def _update_main_models(project_root: Path, app_name: str) -> None:
    """Update the main_models.py file to include the new app's models."""
    main_models_path = project_root / "app" / "core" / "main_models.py"
    
    if not main_models_path.exists():
        typer.echo("Warning: Could not find main_models.py to update. You'll need to manually add the new models.")
        return
    
    with open(main_models_path, 'r') as f:
        lines = f.readlines()
    
    import_line = f"from app.{app_name}.models import *\n"
    
    # Check if import already exists
    if import_line not in lines:
        # Add import at the end of the file
        lines.append(import_line)
    
    with open(main_models_path, 'w') as f:
        f.writelines(lines)

def _print_tree(directory, prefix=""):
    """Print a directory tree structure."""
    typer.echo(f"{directory.name}/")
    
    items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        if is_last:
            item_prefix = prefix.replace("├── ", "└── ")
        else:
            item_prefix = prefix
            
        if item.is_file():
            typer.echo(f"{item_prefix}{item.name}")
