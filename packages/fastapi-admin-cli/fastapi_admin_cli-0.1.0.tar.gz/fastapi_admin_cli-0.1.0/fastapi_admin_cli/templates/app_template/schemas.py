from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class {{ app_class_name }}Base(BaseModel):
    """Base schema for {{ app_class_name }} with common attributes."""
    name: str
    description: Optional[str] = None

class {{ app_class_name }}Create({{ app_class_name }}Base):
    """Schema for creating a new {{ app_class_name }}."""
    pass

class {{ app_class_name }}Update(BaseModel):
    """Schema for updating an existing {{ app_class_name }}."""
    name: Optional[str] = None
    description: Optional[str] = None

class {{ app_class_name }}Read({{ app_class_name }}Base):
    """Schema for reading a {{ app_class_name }} with all attributes."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
