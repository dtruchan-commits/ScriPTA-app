#!/usr/bin/env python3
"""
Test script to verify Databricks connection and query TPM data.
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.databricks import databricks_config, execute_databricks_query


def test_connection():
    """Test basic Databricks connection."""
    print("Testing Databricks connection...")
    try:
        result = execute_databricks_query("SELECT 1 as test_value")
        print("✅ Connection successful!")
        print(f"Test result: {result}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_tpm_query():
    """Test the specific TPM query."""
    print("\nTesting TPM data query...")
    try:
        query = f"""
        SELECT *
        FROM {databricks_config.get_full_table_name('p2r_pnodid_view')}
        WHERE pname LIKE 'TPM%'
        LIMIT 5
        """
        
        print(f"Executing query: {query.strip()}")
        result = execute_databricks_query(query)
        
        print(f"✅ Query successful! Found {len(result)} rows")
        
        if result:
            print("\nFirst row data:")
            for key, value in result[0].items():
                print(f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False


def show_config():
    """Show current Databricks configuration."""
    print("Current Databricks Configuration:")
    print(f"  Server Hostname: {databricks_config.server_hostname}")
    print(f"  HTTP Path: {databricks_config.http_path}")
    print(f"  Catalog: {databricks_config.catalog}")
    print(f"  Schema: {databricks_config.schema}")
    print(f"  Access Token: {'*' * 20}...{databricks_config.access_token[-4:] if databricks_config.access_token else 'Not set'}")
    print()


if __name__ == "__main__":
    print("ScriPTA Databricks Connection Test")
    print("=" * 40)
    
    show_config()
    
    # Test basic connection
    if test_connection():
        # Test TPM query
        test_tpm_query()
    else:
        print("Skipping TPM query test due to connection failure.")
    
    print("\nTest completed.")