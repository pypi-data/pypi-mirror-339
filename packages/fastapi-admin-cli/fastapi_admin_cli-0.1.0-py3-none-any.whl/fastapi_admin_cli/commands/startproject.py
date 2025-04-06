import os
import shutil
from pathlib import Path
import typer
from typing import Optional
from jinja2 import Environment, FileSystemLoader
import importlib.resources as pkg_resources

from fastapi_admin_cli.templates import project_template

def create_new_project(project_name: str, directory: Optional[Path] = None) -> None:
    """
    Create a new FastAPI project with the specified name.
    
    Args:
        project_name: Name of the project to create
        directory: Directory to create the project in (default is current directory)
    """
    # Get the base directory where we'll create the project
    base_dir = Path.cwd() if directory is None else directory
    project_dir = base_dir / project_name
    
    if project_dir.exists():
        if typer.confirm(f"Directory {project_dir} already exists. Do you want to overwrite it?"):
            shutil.rmtree(project_dir)
        else:
            typer.echo("Project creation cancelled.")
            raise typer.Exit(1)
    
    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create templates environment
    template_dir = pkg_resources.files(project_template)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    
    # Context for template rendering
    context = {
        "project_name": project_name,
    }
    
    # Process all template files
    _process_templates(env, context, template_dir, project_dir)
    
    # Copy auth module from the reference implementation
    auth_source = Path(__file__).parent.parent.parent / "auth"
    auth_dest = project_dir / "app" / "auth"
    
    if auth_source.exists():
        shutil.copytree(auth_source, auth_dest)
        typer.echo("Auth module copied successfully")
    else:
        typer.echo("Warning: Auth module source not found", err=True)
    
    # Copy .env.example to project root
    env_example_source = template_dir / ".env.example"
    env_example_dest = project_dir / ".env.example"
    
    if env_example_source.exists():
        # Read .env template
        template = env.get_template(".env")
        # Render with context and write to .env.example
        with open(env_example_dest, 'w', encoding='utf-8') as f:
            f.write(template.render(**context))
        typer.echo(".env.example created successfully")
    
    # Make manage.py executable
    os.chmod(project_dir / "manage.py", 0o755)
    
    typer.echo(f"Creating project structure:")
    _print_tree(project_dir, level=0)

def _process_templates(env, context, template_dir, output_dir, rel_path=""):
    """Process all template files recursively, rendering them with the context."""
    source_dir = template_dir / rel_path
    target_dir = output_dir / rel_path
    
    # Skip __pycache__ and other unwanted directories/files
    if any(part.startswith(('__pycache__', '.', '~')) for part in source_dir.parts):
        return
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for item in source_dir.iterdir():
        # Skip __pycache__, dot files, and other unwanted files
        if item.name.startswith(('__pycache__', '.', '~')) or item.name.endswith(('.pyc', '.pyo')):
            continue
            
        # Use os.path.join and normalize to forward slashes for Jinja
        rel_item_path = os.path.join(rel_path, item.name) if rel_path else item.name
        rel_item_path = rel_item_path.replace('\\', '/')
        
        if item.is_dir():
            # Process subdirectory
            _process_templates(env, context, template_dir, output_dir, rel_item_path)
        else:
            # Process file
            template_file = env.get_template(rel_item_path)
            output_content = template_file.render(**context)
            
            # Get the output file path, handling special filenames
            output_file_path = target_dir / item.name.replace('__project_name__', context['project_name'])
            
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(output_content)

def _print_tree(directory, level=0, prefix=""):
    """Print a directory tree structure."""
    if level == 0:
        typer.echo(f"{directory.name}/")
        prefix = "├── "
    else:
        typer.echo(f"{prefix}{directory.name}/")
        prefix = prefix.replace("├── ", "│   ").replace("└── ", "    ") + "├── "
    
    items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        item_prefix = prefix.replace("├── ", "└── ") if is_last else prefix
        
        if item.is_dir() and not item.name == '__pycache__' and not item.name.startswith('.'):
            _print_tree(item, level + 1, item_prefix)
        elif item.is_file():
            typer.echo(f"{item_prefix}{item.name}")
