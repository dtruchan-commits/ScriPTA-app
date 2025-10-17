"""
In-memory cache manager for masterdata to provide fast access to material data.
This module manages an in-memory SQLite database for ultra-fast material lookups.
"""
import logging
import sqlite3
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class MasterdataCacheManager:
    """Manages in-memory SQLite database for masterdata caching."""
    
    def __init__(self):
        self._memory_db: Optional[sqlite3.Connection] = None
        self._is_initialized = False
    
    def initialize_cache(self) -> None:
        """Initialize the in-memory SQLite database with masterdata table."""
        try:
            # Create in-memory database
            self._memory_db = sqlite3.connect(":memory:", check_same_thread=False)
            
            # Create masterdata_databricks table with same structure as file-based SQLite
            create_table_sql = """
            CREATE TABLE masterdata_databricks (
                MATNR TEXT PRIMARY KEY,
                MATNR8 INTEGER,
                MATERIAL_DESCRIPTION TEXT,
                MATERIAL_TYPE TEXT,
                XPLANT_STATUS TEXT,
                PRDHATXT TEXT,
                MAKEUP TEXT,
                PLANTS TEXT,
                PLANTS_TXT TEXT,
                CONTRACT_MANUFACTURER_CODETYPE TEXT,
                CONTRACT_MANUFACTURER_CODE TEXT,
                RESPONSIBLE_FOR_SPECIFICATION TEXT,
                CONTRACT_MANUFACTURER_MATERIAL TEXT,
                LAYOUT_APPROVED TEXT,
                USAGE_PREFIX TEXT,
                NUMBER_OF_PAGES TEXT,
                ACF_FLAG TEXT,
                VISIBLE_MARKINGS TEXT,
                CODE TEXT,
                COLORS TEXT,
                NUMBER_COLORS_FRONT TEXT,
                CONTRACT_MANUFACTURER TEXT,
                ARTICLE_CODETYPE TEXT,
                ARTICLE_CODE TEXT,
                CONTRACT_MAN_VISIBLE_MARKINGS TEXT,
                CONTRACT_MANUFACTURER_MT_INDEX TEXT,
                COMPONENT_SCRAB_KEY TEXT,
                REMARKS TEXT,
                PRINTED TEXT,
                NUMBER_COLORS_BACK TEXT,
                PRINT_CHARACTERISTICS TEXT,
                BRAILLE_TEXT TEXT,
                PRINTCHAR_BRAILLE TEXT,
                PRINTCHAR_FOILSTAMP TEXT,
                PRINTCHAR_GOLDHOTFOIL TEXT,
                PRINTCHAR_EMBOSSDEBOSS TEXT,
                PRINTCHAR_SPOTVARNISH TEXT,
                PRINTCHAR_SCRATCHOFF TEXT,
                PRINTCHAR_LAMINATION TEXT,
                PRINTCHAR_DIECUT TEXT,
                PRINTCHAR_PERFORATION TEXT,
                PRINTCHAR_GLOSSVARNISH TEXT,
                PRINTCHAR_LEAFLETING TEXT,
                PRINTCHAR_FOLDING TEXT,
                PRINTCHAR_RICHPALEGOLD TEXT,
                PRINTCHAR_SILVERHOTFOIL TEXT,
                PRINTCHAR_UNVARNISH TEXT,
                PRINTCHAR_SECURITYVARISH TEXT,
                PRINTCHAR_MATTVARNISH TEXT,
                PRINTCHAR_CODINGBYSUPPLIER TEXT,
                PRINTCHAR_BKLOGO TEXT,
                PRINTCHAR_S_DR TEXT,
                DRA_COMBINATION TEXT,
                DRA_COMBINATION_DKTXTUC TEXT,
                DRA_DIELINE TEXT,
                DRA_DIELINE_DKTXTUC TEXT,
                DRA_OTHER TEXT,
                DRA_OTHER_DKTXTUC TEXT,
                DRA_ALL TEXT,
                DRA_ALL_DKTXTUC TEXT,
                DRA_1 TEXT,
                DRA_2 TEXT,
                DRA_3 TEXT,
                DRA_4 TEXT,
                DRA_5 TEXT,
                DRA_6 TEXT,
                DRA_7 TEXT,
                DRA_8 TEXT,
                DRA_9 TEXT,
                DRA_10 TEXT,
                LRA TEXT,
                LRA_VERSION TEXT,
                LRA_DATE TEXT,
                LRA_FILENAME TEXT,
                HRL TEXT,
                HRL_VERSION TEXT,
                HRL_DATE TEXT,
                ACS TEXT,
                ACS_VERSION TEXT,
                TPM_DRAWING TEXT,
                TPM TEXT,
                TPMTXT TEXT,
                TPM_STATUS TEXT,
                GLPT TEXT,
                GLPTTXT TEXT,
                ECLASS TEXT,
                ECLASSTXT TEXT,
                ECLASS_S TEXT,
                ECLASS_S_TXT TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor = self._memory_db.cursor()
            cursor.execute(create_table_sql)
            
            # Create indexes for faster lookups
            cursor.execute("CREATE INDEX idx_matnr8 ON masterdata_databricks (MATNR8)")
            cursor.execute("CREATE INDEX idx_matnr ON masterdata_databricks (MATNR)")
            cursor.execute("CREATE INDEX idx_material_type ON masterdata_databricks (MATERIAL_TYPE)")
            
            self._memory_db.commit()
            self._is_initialized = True
            
            logger.info("In-memory masterdata cache initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize in-memory cache: {str(e)}")
            raise
    
    def load_masterdata_from_sqlite(self, sqlite_db_path: str) -> int:
        """Load masterdata from file-based SQLite into in-memory cache."""
        if not self._is_initialized:
            raise RuntimeError("Cache not initialized. Call initialize_cache() first.")
        
        try:
            # Connect to file-based SQLite database
            file_db = sqlite3.connect(sqlite_db_path)
            file_cursor = file_db.cursor()
            
            # Check if masterdata_databricks table exists in file database
            file_cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='masterdata_databricks'
            """)
            
            if not file_cursor.fetchone():
                logger.warning("masterdata_databricks table not found in SQLite database")
                file_db.close()
                return 0
            
            # Fetch all data from file database
            file_cursor.execute("SELECT * FROM masterdata_databricks")
            rows = file_cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in file_cursor.description]
            
            file_db.close()
            
            if not rows:
                logger.warning("No data found in masterdata_databricks table")
                return 0
            
            # Clear existing data in memory cache
            memory_cursor = self._memory_db.cursor()
            memory_cursor.execute("DELETE FROM masterdata_databricks")
            
            # Insert data into memory database
            placeholders = ','.join(['?' for _ in column_names])
            insert_sql = f"INSERT INTO masterdata_databricks ({','.join(column_names)}) VALUES ({placeholders})"
            
            memory_cursor.executemany(insert_sql, rows)
            self._memory_db.commit()
            
            rows_loaded = len(rows)
            logger.info(f"Loaded {rows_loaded} masterdata records into in-memory cache")
            
            return rows_loaded
            
        except Exception as e:
            logger.error(f"Failed to load masterdata from SQLite: {str(e)}")
            raise
    
    def bulk_insert_masterdata(self, masterdata_records: List[Dict]) -> int:
        """Bulk insert masterdata records into in-memory cache."""
        if not self._is_initialized:
            raise RuntimeError("Cache not initialized. Call initialize_cache() first.")
        
        if not masterdata_records:
            return 0
        
        try:
            cursor = self._memory_db.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM masterdata_databricks")
            
            # Prepare insert statement
            # We'll use the first record to get the column names
            first_record = masterdata_records[0]
            columns = list(first_record.keys())
            placeholders = ','.join(['?' for _ in columns])
            insert_sql = f"INSERT OR REPLACE INTO masterdata_databricks ({','.join(columns)}) VALUES ({placeholders})"
            
            # Convert records to tuples
            record_tuples = []
            for record in masterdata_records:
                # Ensure all records have the same columns in the same order
                tuple_data = tuple(record.get(col) for col in columns)
                record_tuples.append(tuple_data)
            
            # Bulk insert
            cursor.executemany(insert_sql, record_tuples)
            self._memory_db.commit()
            
            rows_inserted = len(record_tuples)
            logger.info(f"Bulk inserted {rows_inserted} masterdata records into in-memory cache")
            
            return rows_inserted
            
        except Exception as e:
            logger.error(f"Failed to bulk insert masterdata: {str(e)}")
            raise
    
    def get_masterdata_by_matnr8(self, matnr8: int) -> Optional[Dict]:
        """Get masterdata record by MATNR8 from in-memory cache."""
        if not self._is_initialized:
            raise RuntimeError("Cache not initialized. Call initialize_cache() first.")
        
        try:
            cursor = self._memory_db.cursor()
            cursor.execute("SELECT * FROM masterdata_databricks WHERE MATNR8 = ?", (matnr8,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Convert to dictionary
            return dict(zip(column_names, row))
            
        except Exception as e:
            logger.error(f"Failed to get masterdata by MATNR8 {matnr8}: {str(e)}")
            raise
    
    def get_all_masterdata(self, limit: Optional[int] = None) -> List[Dict]:
        """Get all masterdata records from in-memory cache."""
        if not self._is_initialized:
            raise RuntimeError("Cache not initialized. Call initialize_cache() first.")
        
        try:
            cursor = self._memory_db.cursor()
            
            if limit:
                cursor.execute("SELECT * FROM masterdata_databricks ORDER BY MATNR8 LIMIT ?", (limit,))
            else:
                cursor.execute("SELECT * FROM masterdata_databricks ORDER BY MATNR8")
            
            rows = cursor.fetchall()
            
            if not rows:
                return []
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Convert to list of dictionaries
            return [dict(zip(column_names, row)) for row in rows]
            
        except Exception as e:
            logger.error(f"Failed to get all masterdata: {str(e)}")
            raise
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        if not self._is_initialized:
            return {"initialized": False, "record_count": 0}
        
        try:
            cursor = self._memory_db.cursor()
            cursor.execute("SELECT COUNT(*) FROM masterdata_databricks")
            count = cursor.fetchone()[0]
            
            # Get latest update timestamp
            cursor.execute("SELECT MAX(updated_at) FROM masterdata_databricks")
            last_updated = cursor.fetchone()[0]
            
            return {
                "initialized": True,
                "record_count": count,
                "last_updated": last_updated
            }
            
        except Exception as e:
            logger.error(f"Failed to get cache stats: {str(e)}")
            return {"initialized": True, "record_count": 0, "error": str(e)}
    
    def clear_cache(self) -> None:
        """Clear all data from in-memory cache."""
        if not self._is_initialized:
            return
        
        try:
            cursor = self._memory_db.cursor()
            cursor.execute("DELETE FROM masterdata_databricks")
            self._memory_db.commit()
            logger.info("In-memory cache cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear cache: {str(e)}")
            raise
    
    def close_cache(self) -> None:
        """Close the in-memory database connection."""
        if self._memory_db:
            self._memory_db.close()
            self._memory_db = None
            self._is_initialized = False
            logger.info("In-memory cache closed")


# Global cache manager instance
cache_manager = MasterdataCacheManager()