# pip install pandas openpyxl

import sqlite3
from pathlib import Path

import pandas as pd


def convert_excel_to_sql():
    """
    Extract data from masterdata.xlsx and load it into scripta-db.sqlite3
    """
    # Define file paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    excel_file = script_dir / "masterdata.xlsx"
    db_file = project_root / "scripta-db.sqlite3"
    
    # Check if Excel file exists
    if not excel_file.exists():
        print(f"Error: {excel_file} not found!")
        return False
    
    try:
        # Read Excel file
        print(f"Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)
        print(f"Loaded {len(df)} rows from Excel")
        
        # Connect to SQLite database
        print(f"Connecting to database: {db_file}")
        conn = sqlite3.connect(db_file)
        
        # Create masterdata table (replace if exists)
        print("Creating masterdata table...")
        df.to_sql('masterdata', conn, if_exists='replace', index=False)
        
        # Verify the data was inserted
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM masterdata")
        row_count = cursor.fetchone()[0]
        print(f"Successfully inserted {row_count} rows into masterdata table")
        
        # Show table structure
        cursor.execute("PRAGMA table_info(masterdata)")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Show first 5 rows as sample
        cursor.execute("SELECT * FROM masterdata LIMIT 5")
        sample_rows = cursor.fetchall()
        print(f"\nSample data (first 5 rows):")
        for i, row in enumerate(sample_rows, 1):
            print(f"  Row {i}: {row}")
        
        conn.close()
        print("\nConversion completed successfully!")
        return True
        
    except FileNotFoundError:
        print(f"Error: Excel file {excel_file} not found!")
        return False
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False

if __name__ == "__main__":
    convert_excel_to_sql()
