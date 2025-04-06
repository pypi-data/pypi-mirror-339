"""
This module provides functionality to set up an admin interface for a FastAPI application using SQLAdmin.

It includes a global registry for admin views, a decorator to register admin classes, and a setup function to initialize the admin interface.
"""

from sqladmin import Admin
from app.core.db import engine
from fastapi import FastAPI
from typing import List, Type
from sqladmin.models import ModelView
from pathlib import Path
import os
import importlib

# Global registry to store admin classes
admin_views: List[Type[ModelView]] = []
"""
A global list to store registered admin view classes.

Each class in this list should inherit from `sqladmin.models.ModelView`.
"""

# Decorator function to register admin classes
def register_admin(cls: Type[ModelView]) -> Type[ModelView]:
    """
    Register an admin view class to the global registry.

    Args:
        cls (Type[ModelView]): The admin view class to register.

    Returns:
        Type[ModelView]: The same class that was registered.
    """
    admin_views.append(cls)
    return cls

# Function to set up the admin interface
def setup_admin(app: FastAPI) -> None:
    """
    Initialize the admin interface for the FastAPI application.

    This function creates an instance of `sqladmin.Admin` and adds all registered
    admin views to it. It also imports admin modules to ensure all views are registered.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    admin = Admin(app, engine)
    
    # Try to import all admin modules from the app directory
    app_dir = Path(__file__).parent.parent
    for item in app_dir.iterdir():
        if item.is_dir() and not item.name.startswith('__'):
            admin_path = item / 'admin.py'
            if admin_path.exists():
                module_name = f"app.{item.name}.admin"
                try:
                    importlib.import_module(module_name)
                except ImportError as e:
                    print(f"Could not import admin module {module_name}: {e}")

    for view in admin_views:
        admin.add_view(view)
