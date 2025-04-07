"""
Command to create a new FastAPI application module.
"""
import os
import re
import sys
import logging
from pathlib import Path
from typing import Optional
import typer

from fastapi_admin.utils.template_utils import render_template_directory
from fastapi_admin.utils.file_utils import create_directory

logger = logging.getLogger(__name__)

app = typer.Typer(help="Create a new FastAPI application module.")


def ensure_template_directory_exists():
    """
    Ensure the app template directory exists with necessary files.
    """
    template_dir = Path(__file__).parent.parent / "templates" / "app_template"

    # If template directory doesn't exist or is empty, create a basic structure
    if not template_dir.exists() or not any(template_dir.iterdir()):
        logger.warning(
            "App template directory does not exist or is empty. Creating basic template structure.")
        try:
            # Create directory
            template_dir.mkdir(parents=True, exist_ok=True)

            # Create models.py template
            with open(template_dir / "models.py.tpl", "w") as f:
                f.write('''"""
Database models for the ${app_name} module.
"""
from typing import Optional, List
from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel, Relationship

class ${model_name}(SQLModel, table=True):
    """${model_description}."""
    
    __tablename__ = "${table_name}"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    def __repr__(self) -> str:
        return f"<${model_name} {self.name}>"
''')

            # Create schemas.py template
            with open(template_dir / "schemas.py.tpl", "w") as f:
                f.write('''"""
Pydantic schemas for the ${app_name} module.
"""
from typing import Optional, List
from datetime import datetime
import uuid
from pydantic import BaseModel, Field

# Base schema with common attributes
class ${model_name}Base(BaseModel):
    """Base schema for ${model_name}."""
    name: str
    description: Optional[str] = None

# Schema for creating a new item
class ${model_name}Create(${model_name}Base):
    """Schema for creating a new ${model_name}."""
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example ${model_name}",
                "description": "This is an example"
            }
        }

# Schema for updating an existing item
class ${model_name}Update(BaseModel):
    """Schema for updating an existing ${model_name}."""
    name: Optional[str] = None
    description: Optional[str] = None

# Schema for returning an item
class ${model_name}Read(${model_name}Base):
    """Schema for returning a ${model_name}."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
''')

            # Create services.py template
            with open(template_dir / "services.py.tpl", "w") as f:
                f.write('''"""
Service layer for the ${app_name} module.
"""
from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlmodel import SQLModel

from .models import ${model_name}
from .schemas import ${model_name}Create, ${model_name}Update

class ${model_name}Service:
    """Service for ${model_name} operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: ${model_name}Create) -> ${model_name}:
        """Create a new ${model_name}."""
        db_obj = ${model_name}(**data.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[${model_name}]:
        """Get a ${model_name} by ID."""
        query = select(${model_name}).where(${model_name}.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[${model_name}]:
        """Get all ${model_name_plural}."""
        query = select(${model_name}).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(self, id: uuid.UUID, data: ${model_name}Update) -> Optional[${model_name}]:
        """Update a ${model_name}."""
        obj = await self.get_by_id(id)
        if not obj:
            return None
            
        # Update the object with new values, excluding None values
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        
        # Set updated_at timestamp
        obj.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, id: uuid.UUID) -> bool:
        """Delete a ${model_name}."""
        obj = await self.get_by_id(id)
        if not obj:
            return False
            
        await self.session.delete(obj)
        await self.session.commit()
        return True
''')

            # Create routes.py template
            with open(template_dir / "routes.py.tpl", "w") as f:
                f.write('''"""
API routes for the ${app_name} module.
"""
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from .models import ${model_name}
from .schemas import ${model_name}Read, ${model_name}Create, ${model_name}Update
from .services import ${model_name}Service

# Create a router for this module
router = APIRouter()

@router.post("/", response_model=${model_name}Read, status_code=status.HTTP_201_CREATED)
async def create_${app_name}(
    data: ${model_name}Create,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new ${model_name}.
    """
    service = ${model_name}Service(session)
    return await service.create(data)

@router.get("/{id}", response_model=${model_name}Read)
async def read_${app_name}(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    """
    Get a ${model_name} by ID.
    """
    service = ${model_name}Service(session)
    db_obj = await service.get_by_id(id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="${model_name} not found"
        )
    return db_obj

@router.get("/", response_model=List[${model_name}Read])
async def read_${app_name}_list(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Get a list of ${model_name_plural}.
    """
    service = ${model_name}Service(session)
    return await service.get_all(skip=skip, limit=limit)

@router.patch("/{id}", response_model=${model_name}Read)
async def update_${app_name}(
    id: uuid.UUID,
    data: ${model_name}Update,
    session: AsyncSession = Depends(get_session)
):
    """
    Update a ${model_name}.
    """
    service = ${model_name}Service(session)
    db_obj = await service.update(id, data)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="${model_name} not found"
        )
    return db_obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_${app_name}(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a ${model_name}.
    """
    service = ${model_name}Service(session)
    success = await service.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="${model_name} not found"
        )
''')

            # Create admin.py template
            with open(template_dir / "admin.py.tpl", "w") as f:
                f.write('''"""
Admin interface configuration for the ${app_name} module.
"""
from sqladmin import ModelView
from app.core.main_admin import register_admin
from .models import ${model_name}

@register_admin
class ${model_name}Admin(ModelView, model=${model_name}):
    """Admin view for ${model_name} model."""
    
    name = "${model_name}"
    name_plural = "${model_name_plural}"
    icon = "fa-solid fa-list"
    
    column_list = [
        ${model_name}.id,
        ${model_name}.name,
        ${model_name}.description,
        ${model_name}.created_at,
        ${model_name}.updated_at
    ]
    
    column_searchable_list = [
        ${model_name}.name,
        ${model_name}.description
    ]
    
    column_sortable_list = [
        ${model_name}.name,
        ${model_name}.created_at,
        ${model_name}.updated_at
    ]
    
    column_details_list = [
        ${model_name}.id,
        ${model_name}.name,
        ${model_name}.description,
        ${model_name}.created_at,
        ${model_name}.updated_at
    ]
    
    form_columns = [
        ${model_name}.name,
        ${model_name}.description
    ]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
''')

            # Create __init__.py template
            with open(template_dir / "__init__.py.tpl", "w") as f:
                f.write('''# Import commonly used components for easier imports elsewhere
from .models import ${model_name}
from .schemas import ${model_name}Read, ${model_name}Create, ${model_name}Update
from .services import ${model_name}Service
from .routes import router as ${app_name}_router
''')

            logger.info(f"Created app template structure at {template_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to create app template structure: {str(e)}")
            return False

    return True


@app.callback(invoke_without_command=True)
def main(
    app_name: str = typer.Argument(..., help="Name of the app to create"),
    directory: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Directory where the app will be created"
    ),
):
    """
    Create a new FastAPI application module with the specified name.
    """
    # Validate app name
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', app_name):
        logger.error(
            "App name must start with a letter and contain only letters, numbers, and underscores."
        )
        sys.exit(1)

    # Determine app directory
    if directory:
        app_dir = Path(directory) / app_name
    else:
        # First check if we're inside a project directory
        current_dir = Path.cwd()
        app_module_dir = current_dir / "app"

        if app_module_dir.exists() and app_module_dir.is_dir():
            # We're in the project root, create app in app/
            app_dir = app_module_dir / app_name
        else:
            # Check if we're already in the app directory
            parent_dir = current_dir.parent
            if parent_dir.name == "app" and parent_dir.exists():
                app_dir = parent_dir / app_name
            else:
                # Create in current directory
                app_dir = current_dir / app_name

    # Create app directory
    try:
        create_directory(app_dir)
    except Exception as e:
        logger.error(f"Failed to create app directory: {str(e)}")
        sys.exit(1)

    print(f"Creating app '{app_name}' in {app_dir}...")

    # Get the template directory
    template_dir = Path(__file__).parent.parent / "templates" / "app_template"

    # Ensure template directory exists with necessary files
    if not ensure_template_directory_exists():
        logger.error(
            "Failed to ensure template directory exists with necessary files.")
        sys.exit(1)

    # Get model name (capitalized)
    model_name = "".join(word.capitalize() for word in app_name.split("_"))
    model_name_plural = f"{model_name}s"
    table_name = app_name
    model_description = f"{model_name} model"

    # Define context for template rendering
    context = {
        "app_name": app_name,
        "model_name": model_name,
        "model_name_plural": model_name_plural,
        "table_name": table_name,
        "model_description": model_description,
    }

    # Render templates
    try:
        render_template_directory(
            template_dir,
            app_dir,
            context=context
        )
        print(f"\nApp '{app_name}' created successfully in {app_dir}")
        print("\nRemember to:")
        print(f"1. Add your new app to app/core/main_routes.py:")
        print(f"   from app.{app_name}.routes import {app_name}_router")
        print(
            f"   main_router.include_router({app_name}_router, prefix=f\"/api/{{api_version}}/{app_name}\", tags=[\"{app_name}\"])")
        print(f"2. Add your model to app/core/main_models.py:")
        print(f"   from app.{app_name}.models import {model_name}")
    except Exception as e:
        logger.error(f"Exception during app creation: {e}")
        logger.debug("Detailed error:", exc_info=True)
        sys.exit(1)
