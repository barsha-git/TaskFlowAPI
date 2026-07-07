# TaskFlowAPI

A FastAPI-based REST API for task management with PostgreSQL database and JWT authentication.

## Features

- FastAPI framework for building APIs
- PostgreSQL database with async SQLAlchemy ORM
- JWT-based authentication
- Alembic database migrations
- Docker support with Docker Compose
- Pydantic validation schemas

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic
- **Server**: Uvicorn

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd TaskFlowAPI
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup environment variables

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: A strong secret key for JWT (use `openssl rand -hex 32` to generate)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

### 6. Setup PostgreSQL Database

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up -d
```

**Option B: Manual PostgreSQL Setup**

Ensure PostgreSQL is running and create a database:
```sql
CREATE DATABASE taskflow;
```

### 7. Run database migrations

```bash
alembic upgrade head
```

## Running the Application

Start the development server:

```bash
python main.py
```

Or using Uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
TaskFlowAPI/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database setup
│   ├── model/
│   │   └── user.py            # User model
│   ├── schema/                # Pydantic schemas
│   ├── router/                # API endpoints
│   └── CRUD/                  # CRUD operations
├── alembic/
│   ├── versions/              # Database migrations
│   ├── env.py                 # Alembic environment
│   └── alembic.ini           # Alembic configuration
├── main.py                    # Application entry point
├── docker-compose.yml         # Docker compose configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "migration description"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback to previous migration

```bash
alembic downgrade -1
```

## Development

### Code Style

The project follows PEP 8 standards. Use a linter like `flake8` or `pylint`:

```bash
pip install flake8
flake8 app/
```

### Testing

(Add testing setup as needed)

## Docker

Build and run with Docker:

```bash
docker-compose up --build
```

Stop services:

```bash
docker-compose down
```

View logs:

```bash
docker-compose logs -f
```

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and the `DATABASE_URL` in `.env` is correct.

### Alembic Migration Error

Check that your database is accessible:
```bash
alembic current
```

### Port Already in Use

Change the port in your command:
```bash
uvicorn main:app --reload --port 8001
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please create an issue in the repository.
