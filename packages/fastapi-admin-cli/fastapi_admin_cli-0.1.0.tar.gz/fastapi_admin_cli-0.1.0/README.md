# FastAPI Admin CLI Tool

A command-line tool for creating and managing FastAPI projects with a modular structure inspired by Django's admin.

## Features

- Create new FastAPI projects with a standardized structure
- Add new app modules to existing projects
- Integrated management commands for running servers, migrations, and more
- Automatic admin panel setup with SQLAdmin
- Integration with Alembic for database migrations
- Docker support with Traefik for production deployments
- JWT Authentication built-in
- PostgreSQL with async support
- Email integration ready

## Installation

```bash
# Install from source
git clone https://github.com/amal-babu-git/fastapi-admin-cli.git
cd fastapi-admin-cli
pip install -e .

# Or install directly from PyPI
pip install fastapi-admin-cli
```

## Usage

### Global Commands

These commands can be run from anywhere:

```bash
# Create a new project
fastapi-admin startproject myproject

# Create a new project in a specific directory
fastapi-admin startproject myproject -d /path/to/directory

# Create a new app in an existing project
fastapi-admin startapp users

# Run project management commands
fastapi-admin manage <command> [args]
```

### Project Management Commands

These commands must be run from within a project directory:

```bash
# Run development server
python manage.py runserver
python manage.py runserver --host 0.0.0.0 --port 8080 --no-reload

# Database migrations
python manage.py makemigrations -n "description"  # Create new migrations
python manage.py migrate                          # Apply migrations
python manage.py migrate --revision head          # Migrate to latest

# Interactive shells
python manage.py dbshell    # PostgreSQL shell
python manage.py appshell   # Application container shell

# Create new app
python manage.py startapp users
```

## Project Structure

The tool creates projects with the following structure:

```
myproject/
│
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
├── manage.py           # Project management script
├── README.md
│
├── app/                # Main application package
│   ├── main.py         # FastAPI application entry point
│   │
│   ├── core/           # Core components
│   │   ├── db.py       # Database connection
│   │   ├── settings.py # Application settings
│   │   └── ...         # Other core modules
│   │
│   ├── auth/           # Built-in authentication
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── ...
│   │
│   └── your_apps/      # Your application modules
│
├── docker/             # Docker configuration
│   ├── Dockerfile
│   ├── compose/        # Docker Compose files
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   └── traefik/        # Traefik configuration
│
└── migrations/         # Alembic migrations
```

## App Structure

When you create a new app, it has the following structure:

```
app/myapp/
│
├── __init__.py
├── models.py      # SQLModel models
├── schemas.py     # Pydantic schemas
├── services.py    # Business logic
├── routes.py      # API endpoints
└── admin.py       # Admin panel configuration
```

## Development Flow

1. Create a new project:
   ```bash
   fastapi-admin startproject myproject
   cd myproject
   ```

2. Set up your environment:
   ```bash
   # Copy example env file and edit it
   cp .env.example .env
   ```

3. Create your apps:
   ```bash
   python manage.py startapp users
   python manage.py startapp products
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Start development server:
   ```bash
   python manage.py runserver
   ```

## Docker Development

For development with Docker:
```bash
cd docker/compose
docker-compose up -d
```

For production with Docker and Traefik:
```bash
cd docker/compose
docker-compose -f docker-compose.prod.yml up -d
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Admin Panel: http://localhost:8000/admin

## License

This project is licensed under the MIT License - see the LICENSE file for details.
