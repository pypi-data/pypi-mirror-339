"""
Basic tests for the FastAPI Admin CLI.
"""


def test_version():
    """Ensure we can import and have a version."""
    from fastapi_admin import __version__
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0
