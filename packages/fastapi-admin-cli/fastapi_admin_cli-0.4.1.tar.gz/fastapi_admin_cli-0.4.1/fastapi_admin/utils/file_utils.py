"""
File system utility functions for FastAPI Admin CLI.
"""
import os
import shutil
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_directory(path: Path) -> None:
    """
    Create a directory safely.
    
    Args:
        path: Directory path to create
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {str(e)}")
        raise


def is_fastapi_project() -> bool:
    """
    Check if the current directory is a FastAPI project.
    
    Returns:
        bool: True if the current directory appears to be a FastAPI project
    """
    # Check for app directory and main.py
    app_dir = Path.cwd() / "app"
    main_py = app_dir / "main.py"
    
    # Alternative: Check for pyproject.toml with fastapi dependency
    pyproject_toml = Path.cwd() / "pyproject.toml"
    
    if app_dir.exists() and main_py.exists():
        return True
    
    if pyproject_toml.exists():
        with open(pyproject_toml, 'r') as f:
            content = f.read().lower()
            if "fastapi" in content:
                return True
    
    return False


def copy_directory(src: Path, dest: Path, exclude_patterns=None) -> None:
    """
    Copy directory with optional exclusion patterns.
    
    Args:
        src: Source directory
        dest: Destination directory
        exclude_patterns: List of file/directory patterns to exclude
    """
    if exclude_patterns is None:
        exclude_patterns = []
    
    try:
        if not src.exists():
            logger.error(f"Source directory does not exist: {src}")
            return
        
        if not dest.exists():
            dest.mkdir(parents=True, exist_ok=True)
        
        for item in src.iterdir():
            # Skip excluded patterns
            if any(pattern in item.name for pattern in exclude_patterns):
                logger.info(f"Skipping excluded item: {item}")
                continue
            
            # Create destination path
            dest_path = dest / item.name
            
            if item.is_dir():
                # Recursively copy subdirectory
                copy_directory(item, dest_path, exclude_patterns)
            else:
                # Copy file
                shutil.copy2(item, dest_path)
                logger.info(f"Copied: {item} -> {dest_path}")
    
    except Exception as e:
        logger.error(f"Error copying directory {src} to {dest}: {str(e)}")
        raise


def create_empty_file(path: Path) -> None:
    """
    Create an empty file.
    
    Args:
        path: Path where to create the file
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        logger.info(f"Created empty file: {path}")
    except Exception as e:
        logger.error(f"Failed to create empty file {path}: {str(e)}")
        raise
