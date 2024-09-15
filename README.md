# Student Voter Replication System

## Overview

This system allows the university's student council to upload voter information for the Student Representative Council election. It replicates data from a primary voting system for verification purposes.

### Features:
- Upload CSV/Excel files with student voter data.
- Asynchronous file processing using Celery.
- Pagination and filtering of student data.
- Email notification upon successful data processing.
- Frontend styled with Material-UI.

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- Node.js
- PostgreSQL
- Redis (for Celery)
- Docker (for deployment, optional)

### Backend Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Setup the database in `settings.py`:
    ```bash
    DB_NAME=voting_system_db
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

3. Apply migrations:
    ```bash
    python manage.py migrate
    ```

4. Run Celery worker (in another terminal):
    ```bash
    celery -A core worker --loglevel=info
    ```

5. Start the Django development server:
    ```bash
    python manage.py runserver
    ```

### Frontend Setup

1. Install dependencies:
    ```bash
    npm install
    ```

2. Run the frontend:
    ```bash
    npm start
    ```

### Running Tests

To run unit tests for the backend, use:

```bash
pytest
