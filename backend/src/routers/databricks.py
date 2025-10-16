"""
Databricks router for testing connections and querying data.
"""
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..config.databricks import databricks_config, execute_databricks_query

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