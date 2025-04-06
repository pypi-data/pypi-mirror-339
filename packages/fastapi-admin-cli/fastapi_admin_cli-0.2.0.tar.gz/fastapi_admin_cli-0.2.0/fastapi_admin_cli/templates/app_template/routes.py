from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.core.db import get_session
from .schemas import {{ app_class_name }}Read, {{ app_class_name }}Create, {{ app_class_name }}Update
from .services import {{ app_class_name }}Service

{{ app_name }}_router = APIRouter()
{{ app_name }}_service = {{ app_class_name }}Service()

@{{ app_name }}_router.get("", response_model=List[{{ app_class_name }}Read])
async def get_all_{{ app_name }}(session: AsyncSession = Depends(get_session)) -> List[{{ app_class_name }}Read]:
    """
    Retrieve all {{ app_name }}.
    
    Returns:
        List of all {{ app_name }} ordered by creation date.
    """
    try:
        return await {{ app_name }}_service.get_all(session)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@{{ app_name }}_router.post("", status_code=status.HTTP_201_CREATED, response_model={{ app_class_name }}Read)
async def create_{{ app_name }}(
    item_data: {{ app_class_name }}Create, 
    session: AsyncSession = Depends(get_session)
) -> {{ app_class_name }}Read:
    """
    Create a new {{ app_name }}.
    
    Args:
        item_data: The {{ app_name }} data to create.
        
    Returns:
        The created {{ app_name }}.
    """
    try:
        return await {{ app_name }}_service.create(item_data, session)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Creation failed: {str(e)}"
        )

@{{ app_name }}_router.get("/{item_id}", response_model={{ app_class_name }}Read)
async def get_{{ app_name }}(
    item_id: str, 
    session: AsyncSession = Depends(get_session)
) -> {{ app_class_name }}Read:
    """
    Retrieve a {{ app_name }} by ID.
    
    Args:
        item_id: The unique ID of the {{ app_name }}.
        
    Returns:
        The requested {{ app_name }}.
    """
    try:
        item = await {{ app_name }}_service.get_by_id(item_id, session)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{{ app_class_name }} with ID {item_id} not found"
            )
        return item
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@{{ app_name }}_router.put("/{item_id}", response_model={{ app_class_name }}Read)
async def update_{{ app_name }}(
    item_id: str, 
    item_data: {{ app_class_name }}Update, 
    session: AsyncSession = Depends(get_session)
) -> {{ app_class_name }}Read:
    """
    Update an existing {{ app_name }}.
    
    Args:
        item_id: The unique ID of the {{ app_name }} to update.
        item_data: The updated {{ app_name }} data.
        
    Returns:
        The updated {{ app_name }}.
    """
    try:
        updated_item = await {{ app_name }}_service.update(item_id, item_data, session)
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{{ app_class_name }} with ID {item_id} not found"
            )
        return updated_item
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update: {str(e)}"
        )

@{{ app_name }}_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{{ app_name }}(
    item_id: str, 
    session: AsyncSession = Depends(get_session)
) -> None:
    """
    Delete a {{ app_name }}.
    
    Args:
        item_id: The unique ID of the {{ app_name }} to delete.
    """
    try:
        deleted = await {{ app_name }}_service.delete(item_id, session)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{{ app_class_name }} with ID {item_id} not found"
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete: {str(e)}"
        )
