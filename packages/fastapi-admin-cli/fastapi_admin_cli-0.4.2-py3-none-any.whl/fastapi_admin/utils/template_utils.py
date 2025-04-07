"""
Template rendering utilities for the FastAPI Admin CLI.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from string import Template
import re
import logging
import jinja2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Jinja2 - will be used if available, otherwise fallback to string.Template
try:
    from jinja2 import Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    logger.warning(
        "Jinja2 not available. Using simple template substitution instead.")


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
    if (use_jinja and JINJA2_AVAILABLE):
        env = Environment(autoescape=False)
        template = env.from_string(content)
        return template.render(**context)

    # Otherwise, use basic string.Template
    # Support multiple template formats:
    # 1. ${variable} format - already works with Template
    # 2. {{ variable }} format - needs conversion
    # 3. $variable format - already works with Template

    # Convert {{ variable }} to ${variable} - fixing the regex pattern
    pattern = r"{{(\s*)([a-zA-Z0-9_]+)(\s*)}}"
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

    # Always exclude __pycache__ directories and .pyc files
    exclude.extend(['__pycache__', '*.pyc', '*.pyo',
                   '*.pyd', '.DS_Store', '*.so', '*.dylib'])

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Rendering templates from {src_dir} to {dest_dir}")

    # Process all files and subdirectories
    for item in src_dir.iterdir():
        # Skip excluded patterns - fixed to handle strings safely as glob patterns
        should_exclude = False
        for pattern in exclude:
            try:
                # First try direct string matching
                if pattern in str(item):
                    should_exclude = True
                    break
                # Then try glob-style pattern matching
                if Path(item).match(pattern):
                    should_exclude = True
                    break
            except Exception as e:
                logger.warning(f"Invalid exclude pattern '{pattern}': {e}")

        if should_exclude:
            logger.info(f"Excluding: {item.name}")
            continue

        # Process relative path for destination
        rel_path = item.relative_to(src_dir)
        dest_path = dest_dir / rel_path

        if item.is_dir():
            # Recursively process subdirectory
            render_template_directory(
                item, dest_path, context, exclude, use_jinja, create_init)

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


def render_templates(template_dir: Union[str, Path],
                     target_dir: Union[str, Path],
                     context: Dict[str, Any],
                     exclude: Optional[List[str]] = None) -> None:
    """
    Render templates from a source directory to a target directory.

    Args:
        template_dir: Source directory containing templates
        target_dir: Target directory to write rendered files
        context: Template context variables
        exclude: Optional list of files/patterns to exclude
    """
    template_dir = Path(template_dir)
    target_dir = Path(target_dir)
    exclude = exclude or []

    logger.info(f"Rendering templates from {template_dir} to {target_dir}")

    # Check if template directory exists
    if not template_dir.exists() or not any(template_dir.iterdir()):
        raise FileNotFoundError(
            f"Template directory does not exist or is empty: {template_dir}")

    # Fix: Use safer pattern matching for exclusion
    exclude_patterns = []
    for pattern in exclude or []:
        try:
            if pattern.startswith('^'):
                # This is a regex pattern - try to compile it
                exclude_patterns.append(re.compile(pattern))
            else:
                # This is a glob pattern - use simple string contains
                exclude_patterns.append(pattern)
        except Exception as e:
            logger.warning(f"Skipping invalid pattern '{pattern}': {e}")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        keep_trailing_newline=True,
    )

    # Keep track of any errors
    errors = []

    for root, _, files in os.walk(template_dir):
        rel_dir = os.path.relpath(root, template_dir)
        target_subdir = target_dir / rel_dir if rel_dir != '.' else target_dir

        if not target_subdir.exists():
            target_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_path = Path(root) / file
            rel_path = src_path.relative_to(template_dir)

            # Skip excluded files - improved with safer pattern matching
            should_exclude = False
            for pattern in exclude_patterns:
                if isinstance(pattern, re.Pattern):
                    if pattern.search(str(rel_path)):
                        should_exclude = True
                        break
                elif isinstance(pattern, str) and pattern in str(rel_path):
                    should_exclude = True
                    break

            if should_exclude:
                continue

            # Handle template files with .tpl extension
            if file.endswith('.tpl'):
                dst_file = file[:-4]  # Remove .tpl extension
            else:
                dst_file = file

            dst_path = target_subdir / dst_file

            try:
                # Render the template
                template_path = str(rel_path)
                try:
                    template = env.get_template(template_path)
                    content = template.render(**context)
                except jinja2.exceptions.TemplateNotFound:
                    # If template not found through Jinja loader, read directly
                    with open(src_path, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                    # Use simple template substitution
                    content = render_template(template_content, context)

                # Write the rendered content
                with open(dst_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                logger.debug(f"Created file: {dst_path}")
            except Exception as e:
                error_msg = f"Error rendering template {rel_path}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)

    # If we encountered any errors, raise an exception
    if errors:
        raise Exception(
            f"Encountered {len(errors)} errors while rendering templates. First error: {errors[0]}")
