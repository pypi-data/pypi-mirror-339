"""
Utilities for file operations.
"""
import os
import shutil
import logging
from pathlib import Path
from typing import Union, List, Optional

logger = logging.getLogger(__name__)


def create_directory(directory: Union[str, Path]) -> Path:
    """Create a directory if it doesn't exist."""
    directory = Path(directory)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    return directory


def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> None:
    """Copy a file from source to destination."""
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    # Create parent directories if they don't exist
    destination.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source, destination)
    logger.debug(f"Copied file from {source} to {destination}")


def read_file(file_path: Union[str, Path]) -> str:
    """Read a file and return its contents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path: Union[str, Path], content: str) -> None:
    """Write content to a file."""
    file_path = Path(file_path)

    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.debug(f"Wrote file: {file_path}")


def is_fastapi_project() -> bool:
    """Check if the current directory is a FastAPI project."""
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
    """Copy directory with optional exclusion patterns."""
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
    """Create an empty file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        logger.info(f"Created empty file: {path}")
    except Exception as e:
        logger.error(f"Failed to create empty file {path}: {str(e)}")
        raise
