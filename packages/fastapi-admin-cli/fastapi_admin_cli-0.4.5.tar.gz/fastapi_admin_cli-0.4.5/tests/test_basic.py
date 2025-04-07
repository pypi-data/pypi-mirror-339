"""
Basic tests for the FastAPI Admin CLI.
"""


def test_version():
    """Ensure we can import and have a version."""
    from fastapi_admin import __version__
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_commands_import():
    """Ensure we can import the commands module."""
    from fastapi_admin import commands
    assert commands is not None


def test_project_command_import():
    """Ensure we can import the project command."""
    from fastapi_admin.commands import project
    assert project is not None


def test_app_command_import():
    """Ensure we can import the app command."""
    from fastapi_admin.commands import app
    assert app is not None
