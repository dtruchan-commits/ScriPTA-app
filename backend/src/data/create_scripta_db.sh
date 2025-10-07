#!/bin/bash

# Script to create and populate the ScriPTA SQLite database
# This script creates the scripta-db.sqlite3 database and populates it with data from layers.py and swatches.py

set -e  # Exit on error

DB_NAME="scripta-db.sqlite3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Creating ScriPTA database: $DB_NAME"

# Remove existing database if it exists
if [ -f "$DB_NAME" ]; then
    echo "Removing existing database..."
    rm "$DB_NAME"
fi

# Create the database and tables
echo "Creating database tables..."
sqlite3 "$DB_NAME" << 'EOF'
-- Create layer_config_sets table
CREATE TABLE layer_config_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_name TEXT UNIQUE NOT NULL
);

-- Create layer_config table
CREATE TABLE layer_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_set_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    locked BOOLEAN NOT NULL,
    print BOOLEAN NOT NULL,
    color TEXT NOT NULL,
    FOREIGN KEY (config_set_id) REFERENCES layer_config_sets (id),
    UNIQUE(config_set_id, name)
);

-- Create swatches table
CREATE TABLE swatches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    color_name TEXT UNIQUE NOT NULL,
    color_model TEXT NOT NULL,
    color_space TEXT NOT NULL,
    color_values TEXT NOT NULL  -- JSON array as string
);

-- Create indices for better performance
CREATE INDEX idx_layer_config_set_name ON layer_config_sets(config_name);
CREATE INDEX idx_layer_config_name ON layer_config(name);
CREATE INDEX idx_layer_config_set_id ON layer_config(config_set_id);
CREATE INDEX idx_swatch_color_name ON swatches(color_name);
CREATE INDEX idx_swatch_color_model ON swatches(color_model);
EOF

echo "Tables created successfully."

# Create a Python script to extract and insert the data
echo "Creating data extraction script..."
cat > extract_data.py << 'EOF'
#!/usr/bin/env python3
import sqlite3
import json
import sys
import os

# Add the current directory to the Python path so we can import our modules
sys.path.insert(0, os.getcwd())

from layers import LAYER_DATA
from swatches import SWATCH_DATA

def populate_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Insert layer configuration sets and their layers
        print("Inserting layer configuration data...")
        for layer_set in LAYER_DATA:
            # Insert the configuration set
            cursor.execute(
                "INSERT INTO layer_config_sets (config_name) VALUES (?)",
                (layer_set.config_name,)
            )
            config_set_id = cursor.lastrowid
            
            # Insert each layer in this configuration set
            for layer in layer_set.layers:
                cursor.execute(
                    """INSERT INTO layer_config 
                       (config_set_id, name, locked, print, color) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (config_set_id, layer.name.value, layer.locked, layer.print, layer.color.value)
                )
        
        # Insert swatch data
        print("Inserting swatch configuration data...")
        for swatch in SWATCH_DATA:
            # Convert color_values list to JSON string
            color_values_json = json.dumps(swatch.color_values)
            
            # Handle the Pydantic model attributes properly
            color_model = swatch.color_model if isinstance(swatch.color_model, str) else swatch.color_model.value
            color_space = swatch.color_space if isinstance(swatch.color_space, str) else swatch.color_space.value
            
            cursor.execute(
                """INSERT INTO swatches 
                   (color_name, color_model, color_space, color_values) 
                   VALUES (?, ?, ?, ?)""",
                (swatch.color_name, color_model, color_space, color_values_json)
            )
        
        conn.commit()
        print(f"Successfully inserted {len(LAYER_DATA)} layer configuration sets")
        
        # Count total layers
        total_layers = sum(len(layer_set.layers) for layer_set in LAYER_DATA)
        print(f"Successfully inserted {total_layers} individual layer configurations")
        print(f"Successfully inserted {len(SWATCH_DATA)} swatch configurations")
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_data.py <database_path>")
        sys.exit(1)
    
    db_path = sys.argv[1]
    populate_database(db_path)
EOF

echo "Running data extraction and insertion..."
python3 extract_data.py "$DB_NAME"

# Clean up the temporary extraction script
rm extract_data.py

echo ""
echo "Database creation completed successfully!"
echo "Database file: $DB_NAME"

# Show some statistics
echo ""
echo "Database statistics:"
sqlite3 "$DB_NAME" << 'EOF'
SELECT 'Layer Config Sets: ' || COUNT(*) FROM layer_config_sets;
SELECT 'Layer Configurations: ' || COUNT(*) FROM layer_config;
SELECT 'Swatch Configurations: ' || COUNT(*) FROM swatches;
EOF

echo ""
echo "Sample data verification:"
echo "Layer Config Sets:"
sqlite3 "$DB_NAME" "SELECT config_name FROM layer_config_sets;"

echo ""
echo "First 5 swatches:"
sqlite3 "$DB_NAME" "SELECT color_name, color_model, color_space FROM swatches LIMIT 5;"

echo ""
echo "Database schema:"
sqlite3 "$DB_NAME" ".schema"

echo ""
echo "✅ ScriPTA database created and populated successfully!"
echo "You can now connect to the database using: sqlite3 $DB_NAME"