"""
Template rendering utilities for the FastAPI Admin CLI.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from string import Template
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Jinja2 - will be used if available, otherwise fallback to string.Template
try:
    from jinja2 import Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    logger.warning("Jinja2 not available. Using simple template substitution instead.")


def render_template(content: str, context: Dict[str, Any], use_jinja: bool = False) -> str:
    """
    Render a template string with the given context.
    
    Args:
        content: Template content
        context: Context variables for template rendering
        use_jinja: Whether to use Jinja2 for rendering (if available)
        
    Returns:
        str: Rendered content
    """
    # If Jinja2 is requested and available, use it for rendering
    if use_jinja and JINJA2_AVAILABLE:
        env = Environment(autoescape=False)
        template = env.from_string(content)
        return template.render(**context)
        
    # Otherwise, use basic string.Template 
    # Support multiple template formats:
    # 1. ${variable} format - already works with Template
    # 2. {{ variable }} format - needs conversion
    # 3. $variable format - already works with Template
    
    # Convert {{ variable }} to ${variable}
    pattern = r"{{(\s*)(\w+)(\s*)}}"
    content = re.sub(pattern, r"${\2}", content)
    
    template = Template(content)
    return template.safe_substitute(context)


def render_template_file(src: Path, dest: Path, context: Dict[str, Any], use_jinja: bool = False) -> None:
    """
    Render a template file with the given context.
    
    Args:
        src: Source template file
        dest: Destination file
        context: Context variables for template rendering
        use_jinja: Whether to use Jinja2 for rendering (if available)
    """
    if not src.exists():
        logger.error(f"Template file does not exist: {src}")
        return
    
    # Create parent directories if necessary
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Read template content
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Render template
        rendered_content = render_template(content, context, use_jinja)
        
        # Write rendered content to destination
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        
        logger.info(f"Rendered: {src.name} -> {dest}")
    except Exception as e:
        logger.error(f"Error rendering template {src}: {str(e)}")
        raise


def render_template_directory(
    src_dir: Path, 
    dest_dir: Path, 
    context: Dict[str, Any],
    exclude: List[str] = None,
    use_jinja: bool = False,
    create_init: bool = True
) -> None:
    """
    Render all templates in a directory with the given context.
    
    Args:
        src_dir: Source template directory
        dest_dir: Destination directory
        context: Context variables for template rendering
        exclude: List of patterns to exclude
        use_jinja: Whether to use Jinja2 for rendering (if available)
        create_init: Whether to create __init__.py in dirs without one
    """
    if not src_dir.exists():
        logger.error(f"Template directory does not exist: {src_dir}")
        return
    
    if exclude is None:
        exclude = []
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Rendering templates from {src_dir} to {dest_dir}")
    
    # Process all files and subdirectories
    for item in src_dir.iterdir():
        # Check exclusions
        if any(re.match(pattern, item.name) for pattern in exclude):
            logger.info(f"Excluding: {item.name}")
            continue
        
        # Process relative path for destination
        rel_path = item.relative_to(src_dir)
        dest_path = dest_dir / rel_path
        
        if item.is_dir():
            # Recursively process subdirectory
            render_template_directory(item, dest_path, context, exclude, use_jinja, create_init)
            
            # Create __init__.py if needed
            if create_init and not (item / "__init__.py").exists():
                init_path = dest_path / "__init__.py"
                if not init_path.exists():
                    with open(init_path, 'w') as f:
                        f.write("# Auto-generated __init__.py file\n")
                    logger.info(f"Created: {init_path}")
                    
        else:
            # Render template file
            render_template_file(item, dest_path, context, use_jinja)
