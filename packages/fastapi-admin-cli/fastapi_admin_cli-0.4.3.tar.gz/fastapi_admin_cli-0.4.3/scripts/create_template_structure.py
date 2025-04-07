#!/usr/bin/env python
"""
Create the basic template directory structure for FastAPI Admin CLI.
This ensures that the necessary template files exist for project creation.
"""
import os
import sys
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.resolve()


def create_template_structure():
    """
    Create template directory structure with basic files needed for project creation.
    """
    # Define template base directory
    templates_dir = ROOT_DIR / "fastapi_admin" / "templates"
    project_template_dir = templates_dir / "project_template"
    app_dir = project_template_dir / "app"

    # Create directories
    templates_dir.mkdir(exist_ok=True)
    project_template_dir.mkdir(exist_ok=True)
    app_dir.mkdir(exist_ok=True)

    # Create basic main.py template
    main_py_path = app_dir / "main.py.tpl"
    with open(main_py_path, "w") as f:
        f.write('''"""
Main FastAPI application module.
"""
from fastapi import FastAPI, Depends

app = FastAPI(
    title="${project_name}",
    description="${project_name} API",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to ${project_name}"}
''')

    print(f"Created main.py template at {main_py_path}")

    # Create basic pyproject.toml template
    pyproject_path = project_template_dir / "pyproject.toml.tpl"
    with open(pyproject_path, "w") as f:
        f.write('''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "${project_name}"
version = "0.1.0"
description = "FastAPI project created with fastapi-admin-cli"
requires-python = ">=3.8"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.15.0",
    "sqlmodel>=0.0.8",
    "alembic>=1.10.0",
    "python-jose>=3.3.0",
    "python-multipart>=0.0.5",
    "email-validator>=1.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.0.292",
]

[tool.setuptools]
packages = ["app"]
''')

    print(f"Created pyproject.toml template at {pyproject_path}")

    # Create basic README.md template
    readme_path = project_template_dir / "README.md.tpl"
    with open(readme_path, "w") as f:
        f.write('''# ${project_name}

FastAPI project created with fastapi-admin-cli.

## Getting Started

1. Setup your environment:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -e .
```

2. Run the development server:

```bash
uvicorn app.main:app --reload
# Or
fastapi-admin runserver
```

3. Visit the API documentation at http://localhost:8000/docs
''')

    print(f"Created README.md template at {readme_path}")

    return True


if __name__ == "__main__":
    success = create_template_structure()
    if success:
        print("\nTemplate structure created successfully!")
    else:
        print("\nFailed to create template structure.")
        sys.exit(1)
