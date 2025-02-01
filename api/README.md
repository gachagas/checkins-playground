# Checkins API

A FastAPI application for managing and querying daily checkins data.

## Prerequisites

- Python 3.12+
- [mise](https://mise.jdx.dev/) (recommended for tool version management)
- [Task](https://taskfile.dev/) (for running commands)
- Docker and Docker Compose
- A CSV file containing checkin data (see below)

## Local Setup

1. Install the required tools:
   ```bash
   # If using mise
   mise install

   # Otherwise, install manually:
   # - Python 3.12
   # - Task
   # - uv (Python package manager)
   ```

2. Install dependencies:
   ```bash
   cd api
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. Start the PostgreSQL database:
   ```bash
   task
   ```

4. Run migrations:
   ```bash
   task migrate
   ```

## Loading Checkin Data

1. Create a `.temp` directory in the project root (outside the `api` directory):
   ```bash
   mkdir .temp
   ```

2. Place your checkins CSV file in the `.temp` directory with the name `dailycheckins_minimal.csv`. The CSV should have the following columns:
   ```
   user,timestamp,hours,project
   ```

   Example CSV content:
   ```csv
   user,timestamp,hours,project
   john,2024-02-01 09:00,8.0,Project A
   jane,2024-02-01 09:30,7.5,Project B
   ```

   Note: The timestamp can be in either:
   - ISO format (e.g., "2024-02-01 09:00")
   - Russian format (e.g., "1 февраля 2024 09:00")

3. Load the checkins data:
   ```bash
   cd api
   python src/scripts/load_checkins.py
   ```

## Development

1. Start the API in development mode:
   ```bash
   task api-dev
   ```

2. Access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
api/
├── alembic/              # Database migrations
│   ├── versions/         # Migration version files
│   └── env.py           # Alembic configuration
├── src/
│   ├── models/          # SQLAlchemy database models
│   │   └── checkin.py   # Checkin model definition
│   ├── schemas/         # Pydantic schemas for API
│   │   └── checkin.py   # Checkin-related schemas
│   ├── scripts/         # Utility scripts
│   │   └── load_checkins.py  # Script to load CSV data
│   ├── routes/          # API route handlers
│   ├── database.py      # Database configuration
│   └── main.py          # FastAPI application entry point
├── pyproject.toml       # Project dependencies and configuration
├── alembic.ini          # Alembic migrations configuration
└── README.md           # Project documentation
```

The project follows a modular structure:
- `alembic/`: Handles database migrations and schema changes
- `src/models/`: Contains SQLAlchemy models representing database tables
- `src/schemas/`: Defines Pydantic models for request/response validation
- `src/scripts/`: Contains utility scripts like the CSV data loader
- `src/routes/`: API endpoint handlers (to be implemented)
- `src/database.py`: Database connection and session management
- `src/main.py`: Main FastAPI application with endpoint definitions
