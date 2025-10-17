"""
Databricks router for testing connections and querying data.
"""
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..cache import cache_manager
from ..config.databricks import databricks_config, execute_databricks_query
from .database import create_masterdata_databricks_table, save_masterdata_to_sqlite

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/databricks", tags=["databricks"])


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    data: List[Dict[str, Any]]
    row_count: int
    success: bool


@router.get("/test-connection")
async def test_databricks_connection():
    """Test the Databricks connection."""
    try:
        # Simple query to test connection
        test_query = "SELECT 1 as test_value"
        result = execute_databricks_query(test_query)
        
        return {
            "success": True,
            "message": "Databricks connection successful",
            "config": {
                "server_hostname": databricks_config.server_hostname,
                "catalog": databricks_config.catalog,
                "schema": databricks_config.schema
            },
            "test_result": result
        }
    except Exception as e:
        logger.error(f"Databricks connection test failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Databricks connection failed: {str(e)}"
        )


@router.get("/tpm-data")
async def get_tpm_data(limit: int = Query(default=5, ge=1, le=100)):
    """Get TPM data from the p2r_pnodid_view table."""
    try:
        query = f"""
        SELECT *
        FROM {databricks_config.get_full_table_name('p2r_pnodid_view')}
        WHERE pname LIKE 'TPM%'
        LIMIT {limit}
        """
        
        result = execute_databricks_query(query)
        
        return QueryResponse(
            data=result,
            row_count=len(result),
            success=True
        )
    except Exception as e:
        logger.error(f"Failed to query TPM data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query TPM data: {str(e)}"
        )


@router.post("/execute-query")
async def execute_custom_query(query_request: QueryRequest):
    """Execute a custom SQL query on Databricks."""
    try:
        # Basic validation - only allow SELECT statements for security
        query = query_request.query.strip()
        if not query.upper().startswith("SELECT"):
            raise HTTPException(
                status_code=400,
                detail="Only SELECT queries are allowed"
            )
        
        result = execute_databricks_query(query)
        
        return QueryResponse(
            data=result,
            row_count=len(result),
            success=True
        )
    except Exception as e:
        logger.error(f"Failed to execute query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute query: {str(e)}"
        )


@router.get("/get_all_masterdata_from_databricks_before_startup")
async def get_all_masterdata_from_databricks_before_startup():
    """
    Fetch all masterdata from Databricks using the unified CTE query.
    This endpoint retrieves the complete 100MB dataset for caching purposes.
    Should be called once daily or during backend startup.
    """
    try:
        import os

        # Read the unified CTE query from file
        sql_file_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "databricks_unified_material_data_cte.sql"
        )
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            query = file.read()
        
        logger.info("Starting to fetch all masterdata from Databricks (this may take 15-20 seconds)...")
        
        # Execute the full CTE query
        result = execute_databricks_query(query)
        
        logger.info(f"Successfully fetched {len(result)} masterdata records from Databricks")
        
        return {
            "success": True,
            "message": f"Successfully fetched {len(result)} records from Databricks",
            "record_count": len(result),
            "data": result
        }
    
    except FileNotFoundError:
        logger.error("Unified CTE SQL file not found")
        raise HTTPException(
            status_code=500,
            detail="Unified CTE SQL file not found at expected location"
        )
    except Exception as e:
        logger.error(f"Failed to fetch all masterdata from Databricks: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch all masterdata from Databricks: {str(e)}"
        )


@router.post("/save_masterdata_to_sqlite_and_cache")
async def save_masterdata_to_sqlite_and_cache():
    """
    Fetch all masterdata from Databricks and save it to SQLite database and in-memory cache.
    This is the main endpoint for daily data refresh.
    """
    try:
        # First, ensure the masterdata_databricks table exists
        create_masterdata_databricks_table()
        
        # Fetch data from Databricks
        response = await get_all_masterdata_from_databricks_before_startup()
        
        if not response["success"]:
            raise HTTPException(status_code=500, detail="Failed to fetch data from Databricks")
        
        masterdata_records = response["data"]
        
        # Save to SQLite database
        saved_count = save_masterdata_to_sqlite(masterdata_records)
        
        # Update in-memory cache
        cache_loaded = cache_manager.bulk_insert_masterdata(masterdata_records)
        
        logger.info(f"Successfully saved {saved_count} records to SQLite and loaded {cache_loaded} records into cache")
        
        return {
            "success": True,
            "message": f"Successfully fetched {len(masterdata_records)} records from Databricks, saved {saved_count} to SQLite, and loaded {cache_loaded} into cache",
            "databricks_records": len(masterdata_records),
            "sqlite_records_saved": saved_count,
            "cache_records_loaded": cache_loaded
        }
    
    except Exception as e:
        logger.error(f"Failed to save masterdata: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save masterdata: {str(e)}"
        )


@router.post("/refresh_cache_from_sqlite")
async def refresh_cache_from_sqlite():
    """
    Refresh the in-memory cache from SQLite database.
    Use this if you want to reload cache without fetching from Databricks.
    """
    try:
        import os

        # Load data from SQLite into cache
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "scripta-db.sqlite3")
        rows_loaded = cache_manager.load_masterdata_from_sqlite(db_path)
        
        # Get cache stats
        cache_stats = cache_manager.get_cache_stats()
        
        logger.info(f"Refreshed cache with {rows_loaded} records from SQLite")
        
        return {
            "success": True,
            "message": f"Successfully loaded {rows_loaded} records into cache from SQLite",
            "records_loaded": rows_loaded,
            "cache_stats": cache_stats
        }
        
    except Exception as e:
        logger.error(f"Failed to refresh cache from SQLite: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh cache from SQLite: {str(e)}"
        )


@router.get("/schema-info")
async def get_schema_info():
    """Get information about available tables in the schema."""
    try:
        query = f"SHOW TABLES IN {databricks_config.catalog}.{databricks_config.schema}"
        result = execute_databricks_query(query)
        
        return {
            "success": True,
            "catalog": databricks_config.catalog,
            "schema": databricks_config.schema,
            "tables": result
        }
    except Exception as e:
        logger.error(f"Failed to get schema info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get schema info: {str(e)}"
        )