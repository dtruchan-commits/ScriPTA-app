#!/usr/bin/env python3
import re

# Read the current test_main.py file
with open('/workspaces/swatchworx-app/tests/test_main.py', 'r') as f:
    content = f.read()

# Dictionary to map string values to array values
value_mappings = {
    '"50,50,0,0"': '[50, 50, 0, 0]',
    '"0,24,94,0"': '[0, 24, 94, 0]',
    '"95,20,25,20"': '[95, 20, 25, 20]',
    '"20,90,0,40"': '[20, 90, 0, 40]',
    '"0,30,7,0"': '[0, 30, 7, 0]',
    '"70,0,70,0"': '[70, 0, 70, 0]',
    '"0,100,0,0"': '[0, 100, 0, 0]',
    '"100,45,0,18"': '[100, 45, 0, 18]',
    '"69,94,18,0"': '[69, 94, 18, 0]',
    '"100,0,0,0"': '[100, 0, 0, 0]',
    '"27,4,0,0"': '[27, 4, 0, 0]'
}

# Replace all string color values with arrays
new_content = content
for string_val, array_val in value_mappings.items():
    new_content = new_content.replace(f'== {string_val}', f'== {array_val}')

# Update type check from str to list
new_content = new_content.replace(
    'assert isinstance(swatch["colorValues"], str)',
    'assert isinstance(swatch["colorValues"], list)'
)

# Update the test that checks if all parts are numeric - this needs to be updated
# for list format instead of string format
old_color_values_test = '''            color_values = swatch["colorValues"]
            # Should be comma-separated values
            assert isinstance(color_values, str)
            assert "," in color_values or color_values.isdigit()  # Single value or comma-separated
            
            # Split and check that all parts are numeric
            values = color_values.split(",")
            for value in values:
                assert value.strip().isdigit(), f"Invalid color value: {value}"'''

new_color_values_test = '''            color_values = swatch["colorValues"]
            # Should be a list of integers
            assert isinstance(color_values, list)
            assert len(color_values) > 0
            
            # Check that all values are integers
            for value in color_values:
                assert isinstance(value, int), f"Invalid color value: {value}"
                assert 0 <= value <= 255, f"Color value out of range: {value}"'''

new_content = new_content.replace(old_color_values_test, new_color_values_test)

# Write back to the file
with open('/workspaces/swatchworx-app/tests/test_main.py', 'w') as f:
    f.write(new_content)

print("Successfully updated test file to expect arrays instead of strings!")
