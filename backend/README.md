# ScriPTA Backend

This is the backend component of the ScriPTA application, built with FastAPI.

## Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── src/                    # Source code
│   ├── routers/           # API route handlers
│   ├── models/            # Pydantic models
│   └── data/              # Data configuration and utilities
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── pytest.ini           # Pytest configuration
└── scripta-db.sqlite3    # SQLite database
```

## Running the Application

From the backend directory:

```bash
# Install dependencies
conda install --file requirements.txt

# Run the application
python main.py
```

The API will be available at `http://localhost:8000`

## Running Tests

```bash
# From the backend directory
pytest
```