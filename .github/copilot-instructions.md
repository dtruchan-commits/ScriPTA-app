# ScriPTA AI Assistant Instructions

## Project Overview
ScriPTA is a FastAPI backend that serves swatch and layer configurations as well as TPM and Master Data to Adobe InDesign via ExtendScript.

## Key Architecture Patterns

### Data Flow & Storage Strategy
- **Database as Source of Truth**: SQLite (`scripta-db.sqlite3`) is the primary data store
- **Legacy Data Files**: `data/swatches.py` and `data/layers.py` contain static definitions but are NOT the active data source
- **Database Migration**: Use `create_scripta_db.sh` to rebuild database from Python data files
- **Critical**: Never edit data files directly - update database, then regenerate if needed

### API Design Patterns
- **Dual Parameter Names**: Endpoints support both snake_case (`color_name`) and camelCase (`colorName`) via Pydantic aliases
- **Optional Filtering**: All endpoints support optional filters (e.g., `?colorName=DIELINE`, `?configName=default`)
- **Consistent Response Wrapping**: Responses use container objects (`SwatchConfigResponse`, `LayerConfigSetResponse`)

### Type System & Enums
- **Strict Enum Usage**: `ColorModel`, `ColorSpace`, `LayerName`, `LayerColor` define allowed values
- **Model Configuration**: Pydantic models use `use_enum_values=True` and `populate_by_name=True`
- **Database JSON Storage**: Color values stored as JSON strings, parsed to lists in Python

## Development Workflows

### Environment Setup
```bash
conda create -n scripta python=3.12
conda activate scripta
pip install -r requirements.txt
```

### Running & Testing
```bash
# Start development server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest  # Uses pytest.ini configuration

# Code formatting (follows Black + isort configuration)
black .
isort .
```

### Database Management
```bash
# Rebuild database from Python data files
./create_scripta_db.sh

# Direct database access
sqlite3 scripta-db.sqlite3
```

## ExtendScript Integration

### Connection Pattern
- `frontend.jsx` demonstrates HTTP communication from InDesign to FastAPI
- Uses raw socket connections with HTTP/1.1 protocol
- Test paths: `/get_swatch_config`, `/get_layer_config?configName=default`
- Deployment: Copy to InDesign Scripts folder, access via Scripts panel

### API Endpoints for InDesign
- `/get_swatch_config[?colorName=NAME]` - Color definitions for swatches
- `/get_layer_config[?configName=NAME]` - Layer properties (locked, print, color)
- Interactive docs at `localhost:8000/docs`

## Project-Specific Conventions

### File Organization
- `main.py` - FastAPI app with database functions and endpoints
- `models.py` - Pydantic models and enums (dual snake/camel case support)
- `data/` - Legacy static data definitions (reference only)
- `tests/` - Comprehensive test suite with client fixtures

### Testing Strategy
- **Fixture-based**: `conftest.py` provides `client` fixture for FastAPI testing
- **Data Validation**: Tests verify response structure against static data
- **Endpoint Coverage**: Separate test classes for each major endpoint

### Code Style
- **Black formatter**: Line length 88, Python 3.8+ target
- **Import organization**: isort with Black profile
- **Type hints**: Required for all function signatures
- **Error handling**: HTTPException with descriptive messages

## Common Patterns to Follow

### Adding New Endpoints
1. Define Pydantic response models with enum validation
2. Create database query functions with optional filtering
3. Implement endpoint with proper error handling and documentation
4. Add comprehensive test coverage

### Database Schema Changes
1. Update `create_scripta_db.sh` schema
2. Modify data files if needed for population
3. Update Pydantic models and enums
4. Regenerate database and test endpoints

### ExtendScript Features
- Use raw HTTP/1.1 socket connections for InDesign compatibility
- Provide connection testing UI with configurable endpoints
- Handle URL encoding for special characters in queries