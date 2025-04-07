"""
Git utilities for template management.
"""
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# Default repository URL for templates
DEFAULT_TEMPLATE_REPO_URL = "https://github.com/amal-babu-git/fastapi-admin-cli-template.git"
DEFAULT_TEMPLATE_DIR = Path.home() / ".fastapi-admin-templates"


def clone_or_update_templates(repo_url=None, template_dir=None):
    """
    Clone or update the templates repository.

    Args:
        repo_url: Git repository URL to clone (defaults to DEFAULT_TEMPLATE_REPO_URL)
        template_dir: Local directory where templates should be stored (defaults to ~/.fastapi-admin-templates)

    Returns:
        bool: True if operation was successful, False otherwise
    """
    repo_url = repo_url or DEFAULT_TEMPLATE_REPO_URL
    template_dir = template_dir or DEFAULT_TEMPLATE_DIR

    try:
        # Check if the templates directory already exists
        if template_dir.exists():
            logger.info(f"Updating template repository in {template_dir}")
            # Update the repository
            result = subprocess.run(
                ["git", "pull"],
                cwd=template_dir,
                capture_output=True,
                text=True,
                check=True
            )
            logger.debug(f"Git pull result: {result.stdout}")
        else:
            logger.info(f"Cloning template repository to {template_dir}")
            # Clone the repository
            result = subprocess.run(
                ["git", "clone", repo_url, str(template_dir)],
                capture_output=True,
                text=True,
                check=True
            )
            logger.debug(f"Git clone result: {result.stdout}")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Failed to clone or update templates: {str(e)}")
        return False


def get_template_dir(template_type, template_dir=None):
    """
    Get the path to the specified template type directory.

    Args:
        template_type: Type of template ('app_template' or 'project_template')
        template_dir: Base template directory (defaults to ~/.fastapi-admin-templates)

    Returns:
        Path: Path to the template directory
    """
    template_dir = template_dir or DEFAULT_TEMPLATE_DIR
    return template_dir / template_type
