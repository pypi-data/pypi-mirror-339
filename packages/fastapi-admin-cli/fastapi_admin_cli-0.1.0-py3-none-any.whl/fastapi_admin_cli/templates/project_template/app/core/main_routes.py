# Main routes configuration
from fastapi import APIRouter

main_router = APIRouter()

version = "v1"

# Include routers from all apps
# More routers will be added automatically when creating new apps
