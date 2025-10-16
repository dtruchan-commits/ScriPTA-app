"""
Databricks connection configuration and utilities.
"""
import os
from typing import Optional

from databricks import sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabricksConfig:
    """Configuration class for Databricks connection."""

    def __init__(self):
        self.server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        self.http_path = os.getenv("DATABRICKS_HTTP_PATH")
        self.access_token = os.getenv("DATABRICKS_ACCESS_TOKEN")
        self.catalog = os.getenv("DATABRICKS_CATALOG", "efdataonelh_prd")
        self.schema = os.getenv("DATABRICKS_SCHEMA", "generaldiscovery_masterdata_r")

        # Validate required environment variables
        if not all([self.server_hostname, self.http_path, self.access_token]):
            raise ValueError(
                "Missing required Databricks environment variables. "
                "Please ensure DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, "
                "and DATABRICKS_ACCESS_TOKEN are set in your .env file."
            )

    def get_connection(self):
        """Create and return a Databricks SQL connection."""
        return sql.connect(
            server_hostname=self.server_hostname,
            http_path=self.http_path,
            access_token=self.access_token
        )

    def get_full_table_name(self, table_name: str) -> str:
        """Get the fully qualified table name."""
        return f"{self.catalog}.{self.schema}.{table_name}"


# Global configuration instance
databricks_config = DatabricksConfig()


def get_databricks_connection():
    """Get a Databricks connection."""
    return databricks_config.get_connection()


def execute_databricks_query(query: str, params: Optional[list] = None):
    """
    Execute a query on Databricks and return results.

    Args:
        query (str): SQL query to execute
        params (list, optional): Parameters for parameterized queries

    Returns:
        List of dictionaries representing rows
    """
    connection = get_databricks_connection()
    try:
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        # Fetch all rows and convert to list of dictionaries
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))

        return result
    finally:
        connection.close()
