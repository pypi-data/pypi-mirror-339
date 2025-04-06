# app/core/main_models.py
# Import all models here for Alembic to detect them
from sqlmodel import SQLModel

# Import auth models
from app.auth.models import User

# Import models from all apps
# More imports will be added automatically when creating new apps
