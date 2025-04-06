import uuid
from datetime import datetime
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel

class {{ app_class_name }}(SQLModel, table=True):
    __tablename__ = "{{ app_name }}"
    
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(index=True)
    description: Optional[str] = None
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))

    def __repr__(self):
        return f"<{{ app_class_name }} {self.name}>"
