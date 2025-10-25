"""
Example script showing how to load menu data from a CSV file.

Your CSV file should have these columns:
- FROM_MENU: The parent menu name
- TO_MENU: The child menu/program name (empty for headers)
- DESCRIPTION: Description text
- MENU_ORDER: Order of items in the menu
- HEADER_ORDER: Order of headers (when TO_MENU is empty)
- (Optional) USER_TYPE: User type that can access this item

Format example:
FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER;USER_TYPE
MENU1;;Header example;1;1;Admin
MENU1;PROG1;Example desc1;1;9;Admin
MENU1;PROG2;Example desc2;2;9;User
"""

import pandas as pd
from app import app, build_tree

# Load your CSV file
# df = pd.read_csv('your_menu_data.csv', sep=';')

# Example inline data
from io import StringIO
data = """FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER;USER_TYPE
MENU1;;Header example;1;1;Admin
MENU1;PROG1;Example desc1;1;9;Admin
MENU1;PROG2;Example desc2;2;9;User
MENU1;MENU2;Submenu access;3;9;Admin
MENU1;;Subheader example;4;1;Admin
MENU1;PROG3;Example desc3;4;9;User
MENU2;;Header for menu2;1;1;Admin
MENU2;PROG1;Program 1;1;9;Admin
MENU2;PROG2;Program 2;2;9;User"""


df = pd.read_csv(StringIO(data), sep=';')

# Clean up column names (lowercase and strip whitespace)
df.columns = df.columns.str.strip().str.lower()

# Replace empty strings with None for to_menu
df['to_menu'] = df['to_menu'].replace('', None)

# If your CSV doesn't have a user_type column, add one:
# df['user_type'] = 'Admin'

print(f"Loaded {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print(f"\nSample data:")
print(df.head(10))

# Update the app's global dataframe
app.config['df'] = df

# The application will now use this data
# Run with: uv run python load_csv_example.py
if __name__ == '__main__':
    # Test the tree building
    tree = build_tree(df)
    print(f"\nBuilt tree with {len(tree)} root nodes")

    # Start the web server
    app.run(debug=True, port=5000)
