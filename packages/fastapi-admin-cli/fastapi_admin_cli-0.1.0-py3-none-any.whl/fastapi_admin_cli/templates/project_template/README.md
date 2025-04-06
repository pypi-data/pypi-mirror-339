# {{ project_name }} API

A modern RESTful API built with FastAPI.

## Features

- FastAPI with SQLModel for enhanced type safety
- JWT Authentication with fastapi-users
- SQLAdmin for automatic admin panel
- PostgreSQL database with async support
- Email verification
- Docker support with Traefik for secure HTTPS
- Alembic for database migrations

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (or use the provided Docker service)

### Development Setup

1. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -e .
   ```
3. Create a `.env` file with the required environment variables (see .env file)
4. Run the development server:
   ```
   python manage.py runserver
   ```

### Using Docker

For development with Docker:
```
cd docker/compose
docker-compose up -d
```

For production with Docker:
```
cd docker/compose
docker-compose -f docker-compose.prod.yml up -d
```

### Production Deployment

For a proper production deployment:

1. Update the `.env` file with appropriate production values:
   - Set strong, unique values for `SECRET_KEY` and `JWT_SECRET`
   - Configure your production domain in `API_DOMAIN`
   - Set up proper Traefik dashboard credentials
   - Configure proper SMTP settings

2. Set appropriate permissions for Traefik's ACME storage:
   ```
   mkdir -p docker/traefik/letsencrypt
   touch docker/traefik/acme.json
   chmod 600 docker/traefik/acme.json
   ```

3. Deploy with Docker Compose:
   ```
   cd docker/compose
   docker-compose -f docker-compose.prod.yml up -d
   ```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Admin Panel

The admin panel is available at http://localhost:8000/admin

## Managing Your Project

### Creating a New App

```bash
python manage.py startapp your_app_name
```

### Running Migrations

To create new migrations:
```bash
python manage.py makemigrations -n "description_of_changes"
```

To apply migrations:
```bash
python manage.py migrate
```

### Interactive Shell

```bash
python manage.py shell
```

## Project Structure

```
{{ project_name }}/
│
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
├── manage.py            # Project management script
├── README.md
│
├── app/                 # Main application package
│   ├── main.py          # FastAPI application entry point
│   │
│   ├── core/            # Core components
│   │   ├── db.py        # Database connection
│   │   ├── settings.py  # Application settings
│   │   └── ...          # Other core modules
│   │
│   └── your_apps/       # Your application modules
│
├── docker/              # Docker configuration
│   ├── Dockerfile
│   ├── compose/         # Docker Compose files
│   └── traefik/         # Traefik configuration
│
└── migrations/          # Alembic migrations
```
