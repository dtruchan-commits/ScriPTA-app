# SwatchWorx API

A FastAPI backend application that provides swatch configuration data.

## Features

- FastAPI backend with type safety using Pydantic models
- `/get_swatch_config` endpoint that returns hardcoded swatch configuration
- Proper type definitions using Enums for Color Model and Color Space
- JSON response format with structured data

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

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

Returns swatch configuration data in JSON format.

**Response format:**
```json
{
  "swatches": [
    {
      "colorname": "DIELINE",
      "color_model": "SPOT",
      "color_space": "CMYK",
      "colorvalues": "0,50,100,0"
    },
    {
      "colorname": "PA123",
      "color_model": "SPOT", 
      "color_space": "CMYK",
      "colorvalues": "50,50,50,50"
    },
    {
      "colorname": "PA321",
      "color_model": "PROCESS",
      "color_space": "CMYK", 
      "colorvalues": "40,40,40,40"
    }
  ]
}
```

## Project Structure

```
swatchworx-app/
├── main.py          # FastAPI application and endpoints
├── models.py        # Pydantic models and type definitions
├── data.py          # Hardcoded swatch data
├── requirements.txt # Python dependencies
└── README.md       # This file
```
