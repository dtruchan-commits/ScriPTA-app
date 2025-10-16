import os
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine, text

load_dotenv()

router = APIRouter(prefix="/api/masterdata", tags=["masterdata"])

def get_hana_connection():
    """Create connection to HANA database"""
    try:
        connection_string = f"hana+pyhdb://{os.getenv('HANA_USERNAME')}:{os.getenv('HANA_PASSWORD')}@{os.getenv('HANA_HOST')}:{os.getenv('HANA_PORT')}/{os.getenv('HANA_DATABASE')}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@router.get("/test-connection")
async def test_hana_connection() -> Dict[str, Any]:
    """
    Test HANA database connection with the specific products table
    """
    try:
        engine = get_hana_connection()
        
        # Test query using the specific table structure
        query = """
        SELECT * FROM RXWSSTD."products.wsstd.dv.pmd::DV_MARA" 
        LIMIT 5
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(query))
            
            # Convert to list of dictionaries
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            
            return {
                "status": "success",
                "message": "Connection successful",
                "data": data,
                "column_count": len(columns),
                "row_count": len(data),
                "columns": list(columns)
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection test failed: {str(e)}",
            "data": None
        }

@router.get("/")
async def get_masterdata(
    limit: int = 100,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Fetch material masterdata from HANA Database DS21
    """
    try:
        engine = get_hana_connection()
        
        # Updated query using the correct table name
        query = """
        SELECT *
        FROM RXWSSTD."products.wsstd.dv.pmd::DV_MARA" 
        ORDER BY MATNR
        LIMIT :limit OFFSET :offset
        """
        
        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                {"limit": limit, "offset": offset}
            )
            
            # Convert to list of dictionaries
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            
            return {
                "masterdata": data,
                "count": len(data),
                "limit": limit,
                "offset": offset
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch material masterdata: {str(e)}")

@router.get("/{material_number}")
async def get_material_by_number(material_number: str) -> Dict[str, Any]:
    """
    Fetch specific material by material number
    """
    try:
        engine = get_hana_connection()
        
        # Convert input to integer for proper matching
        try:
            material_int = int(material_number)
        except ValueError:
            raise HTTPException(status_code=400, detail="Material number must be numeric")
        
        query = """
        SELECT *
        FROM RXWSSTD."products.wsstd.dv.pmd::DV_MARA" 
        WHERE MATNR = :material_number OR MATNR8 = :material_number
        LIMIT 10
        """
        
        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                {"material_number": material_int}
            )
            
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            
            if not data:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Material number '{material_number}' not found"
                )
            
            return {
                "data": data,
                "count": len(data),
                "search_term": material_number
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch material: {str(e)}")

@router.get("/search")
async def search_materials(
    query: str,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Search materials by description or material number
    """
    try:
        engine = get_hana_connection()
        
        search_query = """
        SELECT *
        FROM RXWSSTD."products.wsstd.dv.pmd::DV_MARA" 
        WHERE UPPER(materialDescription) LIKE UPPER(:search_pattern)
           OR CAST(MATNR AS VARCHAR) LIKE :number_pattern
           OR CAST(MATNR8 AS VARCHAR) LIKE :number_pattern
        ORDER BY MATNR
        LIMIT :limit
        """
        
        with engine.connect() as connection:
            result = connection.execute(
                text(search_query),
                {
                    "search_pattern": f"%{query}%",
                    "number_pattern": f"%{query}%",
                    "limit": limit
                }
            )
            
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            
            return {
                "data": data,
                "count": len(data),
                "search_query": query,
                "limit": limit
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/debug/search/{material_number}")
async def debug_material_search(material_number: str) -> Dict[str, Any]:
    """
    Debug endpoint to see different search patterns for material number
    """
    try:
        engine = get_hana_connection()
        
        # Try multiple search patterns
        patterns = [
            f"%{material_number}%",  # Contains anywhere
            f"{material_number}%",   # Starts with
            f"%{material_number}",   # Ends with
            f"%{material_number.zfill(18)}%",  # Zero-padded to 18 chars
            f"%{material_number.zfill(10)}%",  # Zero-padded to 10 chars
        ]
        
        results = {}
        
        for i, pattern in enumerate(patterns):
            query = """
            SELECT MATNR, COUNT(*) as count
            FROM RXWSSTD."products.wsstd.dv.pmd::DV_MARA" 
            WHERE MATNR LIKE :pattern
            GROUP BY MATNR
            LIMIT 10
            """
            
            with engine.connect() as connection:
                result = connection.execute(text(query), {"pattern": pattern})
                data = [dict(zip(result.keys(), row)) for row in result.fetchall()]
                results[f"pattern_{i+1}_{pattern}"] = data
        
        return {
            "search_term": material_number,
            "patterns_tested": patterns,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug search failed: {str(e)}")
