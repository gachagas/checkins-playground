# Checkins Dashboard

A full-stack application for managing and visualizing daily checkins data, built with FastAPI and SvelteKit.

## Prerequisites
- Python 3.12+ (recommended to use [mise](https://mise.jdx.dev/) or [pyenv](https://github.com/pyenv/pyenv))
- [Task](https://taskfile.dev/) for running commands
- Docker and Docker Compose
- Ensure you have copy of checkins locally in the `.temp/dailycheckins.csv` folder in the root of the project.

## Quick Start


1. **Set up the data directory:**
   ```bash
   mkdir .temp
   ```

2. **Place your checkins CSV file at `.temp/dailycheckins.csv` with the following structure:**
   ```csv
   user,timestamp,hours,project
   john,2024-02-01 09:00,8.0,Project A
   jane,2024-02-01 09:30,7.5,Project B
   ```

   Note: The timestamp can be in either:
   - ISO format (e.g., "2024-02-01 09:00")
   - Russian format (e.g., "1 февраля 2024 09:00")

3. **Initialize the database and load data:**
   ```bash
   # This will:
   # - Remove existing DB (if any)
   # - Create a new DB
   # - Apply migrations
   # - Load data from CSV

   task reload-fixtures
   ```

5. **Start the services:**
   ```bash
   # Terminal 1: Start API server
   task api-dev

   # Terminal 2: Start UI development server
   task ui-dev
   ```

## Accessing the Application

- **UI:** [http://localhost:3000](http://localhost:3000)
- **API Documentation:**
  - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

