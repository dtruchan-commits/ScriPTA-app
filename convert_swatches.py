#!/usr/bin/env python3
import re

# Read the current swatches.py file
with open('/workspaces/swatchworx-app/data/swatches.py', 'r') as f:
    content = f.read()

# Use regex to find and replace color_values strings with lists
# Pattern matches: color_values="digits,digits,digits,digits"
pattern = r'color_values="([0-9,]+)"'

def replace_color_values(match):
    values_str = match.group(1)
    # Split by comma and convert to integers
    values = [int(x.strip()) for x in values_str.split(',')]
    # Return as list format
    return f'color_values={values}'

# Replace all occurrences
new_content = re.sub(pattern, replace_color_values, content)

# Write back to the file
with open('/workspaces/swatchworx-app/data/swatches.py', 'w') as f:
    f.write(new_content)

print("Successfully converted all color_values from strings to lists!")
