# SwatchWorx API

A simple FastAPI backend application that provides swatch configuration data.

## Features

- FastAPI backend with basic type safety using Pydantic models
- `/get_swatch_config` endpoint that returns swatch configuration data
- Optional filtering by colorname parameter
- Basic error handling for non-existent colornames
- Type definitions using Enums for Color Model and Color Space
- JSON response format with structured data

## Installation

1. Set up conda environment:
```bash
conda init
conda create -n swa python=3.12
conda activate swa
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install development dependencies:
```bash
pip install black isort flake8 mypy
```

4. VSCode Extensions (Recommended):
    - Python (Microsoft) - Core Python support
    - Python Debugger (Microsoft) - Debugging support
    - Pylance (Microsoft) - Language server with IntelliSense
    - Python Environments (Microsoft) - Environment management
    - Black Formatter (Microsoft) - Code formatting
    - isort (Microsoft) - Import sorting
    - Flake8 (Microsoft) - Linting
    - Mypy Type Checker (Microsoft) - Static type checking
    - Prettify JSON (Mohsen Azimi)

## Running the Application

1. Start the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the API:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - OpenAPI schema: http://localhost:8000/openapi.json

## API Endpoints

### GET /get_swatch_config

Returns swatch configuration data in JSON format. Optionally accepts a `colorname` query parameter to filter results.

**Parameters:**
- `colorname` (optional): Filter results by specific colorname (e.g., "DIELINE", "PA123")

**Examples:**

Get all swatches:
```bash
GET /get_swatch_config
```

Get specific swatch:
```bash
GET /get_swatch_config?colorname=DIELINE
```

**Response format for filtered request:**
```json
{
  "swatches": [
    {
      "colorName": "DIELINE",
      "colorModel": "SPOT",
      "colorSpace": "CMYK",
      "colorValues": "0,50,100,0"
    }
  ]
}
```

**Response format for all swatches:**
```json
{
  "swatches": [
    {
      "colorName": "DIELINE",
      "colorModel": "SPOT",
      "colorSpace": "CMYK",
      "colorValues": "0,50,100,0"
    },
    {
      "colorName": "PA123",
      "colorModel": "SPOT", 
      "colorSpace": "CMYK",
      "colorValues": "50,50,50,50"
    },
    {
      "colorName": "PA321",
      "colorModel": "PROCESS",
      "colorSpace": "CMYK", 
      "colorValues": "40,40,40,40"
    }
  ]
}
```

**Error handling:**
- Returns 404 status code with error message if colorname is not found

## Project Structure

```
swatchworx-app/
├── main.py          # FastAPI application and endpoints
├── models.py        # Pydantic models and type definitions  
├── data.py          # Sample swatch data
├── requirements.txt # Python dependencies
└── README.md       # Documentation
```

## Implementation Notes

This is a basic implementation that currently uses hardcoded swatch data. The filtering functionality works by matching the exact colorname provided in the query parameter. Error handling is minimal but functional for the current use case.
