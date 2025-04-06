from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .models import {{ app_class_name }}
from .schemas import {{ app_class_name }}Create, {{ app_class_name }}Update, {{ app_class_name }}Read

class {{ app_class_name }}Service:
    """Service for managing {{ app_name }} operations in the database."""
    
    async def get_all(self, session: AsyncSession) -> List[{{ app_class_name }}Read]:
        """
        Retrieve all {{ app_name }} from the database.
        
        Args:
            session: The database session.
            
        Returns:
            List of {{ app_class_name }} objects ordered by creation date (newest first).
        """
        query = select({{ app_class_name }}).order_by({{ app_class_name }}.created_at.desc())
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, item_id: str, session: AsyncSession) -> Optional[{{ app_class_name }}Read]:
        """
        Retrieve a {{ app_name }} by its ID.
        
        Args:
            item_id: The unique ID of the {{ app_name }}.
            session: The database session.
            
        Returns:
            The {{ app_class_name }} object if found, None otherwise.
        """
        query = select({{ app_class_name }}).where({{ app_class_name }}.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, item_data: {{ app_class_name }}Create, session: AsyncSession) -> {{ app_class_name }}Read:
        """
        Create a new {{ app_name }} in the database.
        
        Args:
            item_data: The {{ app_name }} data to create.
            session: The database session.
            
        Returns:
            The created {{ app_class_name }} object.
            
        Raises:
            SQLAlchemyError: If there's a database error during creation.
        """
        db_item = {{ app_class_name }}(**item_data.model_dump())
        
        try:
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            await session.rollback()
            raise SQLAlchemyError(f"Failed to create {{ app_name }}: {str(e)}") from e
    
    async def update(self, item_id: str, item_update: {{ app_class_name }}Update, session: AsyncSession) -> Optional[{{ app_class_name }}Read]:
        """
        Update an existing {{ app_name }} in the database.
        
        Args:
            item_id: The unique ID of the {{ app_name }} to update.
            item_update: The {{ app_name }} data to update.
            session: The database session.
            
        Returns:
            The updated {{ app_class_name }} object if found, None if {{ app_name }} doesn't exist.
            
        Raises:
            SQLAlchemyError: If there's a database error during update.
        """
        try:
            item = await self._get_item(item_id, session)
            if not item:
                return None
                
            # Update only fields that are provided
            update_data = item_update.model_dump(exclude_unset=True)
            
            # Always update the updated_at timestamp
            update_data["updated_at"] = datetime.now()
            
            for key, value in update_data.items():
                setattr(item, key, value)
                
            await session.commit()
            await session.refresh(item)
            return item
            
        except SQLAlchemyError as e:
            await session.rollback()
            raise SQLAlchemyError(f"Failed to update {{ app_name }} {item_id}: {str(e)}") from e

    async def delete(self, item_id: str, session: AsyncSession) -> bool:
        """
        Delete a {{ app_name }} from the database.
        
        Args:
            item_id: The unique ID of the {{ app_name }} to delete.
            session: The database session.
            
        Returns:
            True if {{ app_name }} was deleted, False if {{ app_name }} doesn't exist.
            
        Raises:
            SQLAlchemyError: If there's a database error during deletion.
        """
        try:
            item = await self._get_item(item_id, session)
            if not item:
                return False
            
            await session.delete(item)
            await session.commit()
            return True
            
        except SQLAlchemyError as e:
            await session.rollback()
            raise SQLAlchemyError(f"Failed to delete {{ app_name }} {item_id}: {str(e)}") from e
    
    async def _get_item(self, item_id: str, session: AsyncSession) -> Optional[{{ app_class_name }}]:
        """
        Helper method to get a {{ app_name }} by ID.
        
        Args:
            item_id: The unique ID of the {{ app_name }}.
            session: The database session.
            
        Returns:
            The {{ app_class_name }} object if found, None otherwise.
        """
        query = select({{ app_class_name }}).where({{ app_class_name }}.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
