import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.cache import cache_manager
from src.routers import databricks, layers, masterdata_sqlite, swatches, tpm, utility
from src.routers.database import (
    create_masterdata_databricks_table,
    get_masterdata_databricks_stats,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for the FastAPI application."""
    # Startup
    logger.info("Starting ScriPTA backend...")
    
    try:
        # Initialize the in-memory cache
        cache_manager.initialize_cache()
        logger.info("In-memory cache initialized")
        
        # Ensure masterdata_databricks table exists in SQLite
        create_masterdata_databricks_table()
        logger.info("masterdata_databricks table ensured in SQLite")
        
        # Check if we have data in SQLite to load into cache
        sqlite_stats = get_masterdata_databricks_stats()
        
        if sqlite_stats["table_exists"] and sqlite_stats["record_count"] > 0:
            # Load data from SQLite into in-memory cache
            db_path = os.path.join(os.path.dirname(__file__), "scripta-db.sqlite3")
            rows_loaded = cache_manager.load_masterdata_from_sqlite(db_path)
            logger.info(f"Loaded {rows_loaded} masterdata records from SQLite into in-memory cache")
            
            # Get cache stats
            cache_stats = cache_manager.get_cache_stats()
            logger.info(f"Cache statistics: {cache_stats}")
        else:
            logger.warning("No masterdata found in SQLite database. Cache will be empty until data is loaded.")
            logger.info("Use the /databricks/save_masterdata_to_sqlite_and_cache endpoint to load data")
        
        logger.info("ScriPTA backend startup completed successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        # Don't fail startup if cache initialization fails
        # The application can still work without the cache
        
    yield
    
    # Shutdown
    logger.info("Shutting down ScriPTA backend...")
    try:
        cache_manager.close_cache()
        logger.info("In-memory cache closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
    
    logger.info("ScriPTA backend shutdown completed")

app = FastAPI(
    title="ScriPTA",
    description="REST API for managing Technical Packaging Material Data and InDesign Swatch and Layer Configurations",
    version="1.0.1",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(utility.router)
app.include_router(swatches.router)
app.include_router(layers.router)
app.include_router(tpm.router)
app.include_router(masterdata_sqlite.router)
app.include_router(databricks.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
