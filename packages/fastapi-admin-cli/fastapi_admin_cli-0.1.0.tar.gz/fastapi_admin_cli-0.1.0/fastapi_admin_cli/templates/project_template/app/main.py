from fastapi import FastAPI, status, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.main_routes import main_router
from app.core.settings import settings
from app.core.db import init_db
from app.core.main_admin import setup_admin
from app.auth.routes import auth_router, users_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def life_span(app: FastAPI):
    # Initialize the database connection
    logger.info("Database initialization starting...")
    await init_db()
    logger.info("Database initialized successfully")
    logger.info("Server starting up...")
    yield
    # Cleanup code can go here if needed
    logger.info("Server shutting down...")

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=life_span,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Background tasks middleware
@app.middleware("http")
async def add_background_tasks_to_request(request: Request, call_next):
    # Add background_tasks to request state
    request.state.background_tasks = BackgroundTasks()
    response = await call_next(request)
    
    # Run background tasks after response is generated
    await request.state.background_tasks()
    return response

# Setup admin before including other routes
setup_admin(app)

# Include auth routers first
app.include_router(auth_router)
app.include_router(users_router)

app.include_router(main_router)


@app.get("/health", tags=["root"], status_code=status.HTTP_200_OK)
async def health_check():
    return {"message": "Welcome to the {{ project_name }} API!"}
