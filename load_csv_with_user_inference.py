"""
Example script for loading menu data where user types are inferred from starting menus.

In AS/400 systems, users are assigned starting menus (like ADMINMENU, USERMENU).
All programs accessible from a starting menu should be tagged with that user type.

For example:
- ADMINMENU -> Can access its own programs + USERMENU programs
- USERMENU -> Can only access USERMENU programs

So USERMENU programs get tagged with both 'Admin' and 'User'
"""

import pandas as pd
from io import StringIO
from collections import defaultdict, deque

# Define starting menus and their corresponding user types
START_MENUS = {
    'ADMINMENU': 'Admin',
    'USERMENU': 'User',
    'TESTUSERMENU': 'TestUser'
}

# Example data
data = """FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER
ADMINMENU;;Header example;1;1
ADMINMENU;ADMPROG1;Example desc1;1;9
ADMINMENU;ADMPROG2;Example desc2;2;9
ADMINMENU;USERMENU;Submenu access;3;9
ADMINMENU;;Subheader example;4;1
ADMINMENU;ADMPROG3;Example desc3;4;9
USERMENU;;Header for USERMENU;1;1
USERMENU;PROG1;Program 1;1;9
USERMENU;PROG2;Program 2;2;9
USERMENU;USERMENU2;Usermenu 2;3;9
USERMENU;PROG5;Program 5!;4;9
USERMENU2;;Header for USERMENU2;1;1
USERMENU2;PROG3;Program 3;1;9
USERMENU2;PROG4;Program 4;2;9
USERMENU2;USERMENU3;Deep Submenu;3;9
USERMENU3;PROG5;Program 5;1;9
TESTUSERMENU;;Header for TESTUSERMENU;1;1
TESTUSERMENU;PROG3;Program 3;1;9
TESTUSERMENU;PROG4;Program 4;2;9
TESTUSERMENU;SUBMENU;Program 4;3;9
SUBMENU;PROG3;Program 3;1;9
SUBMENU;PROG4;Program 4;2;9
"""

# Load the data
df = pd.read_csv(StringIO(data), sep=';')
df.columns = df.columns.str.strip().str.lower()
df['to_menu'] = df['to_menu'].replace('', None)


def find_accessible_menus(df, start_menu):
    """
    Find all menus and programs accessible from a starting menu.
    Uses BFS to traverse the menu tree.
    """
    accessible = set()
    queue = deque([start_menu])
    visited = set()

    while queue:
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)
        accessible.add(current)

        # Find all children of current menu
        children = df[df['from_menu'] == current]['to_menu'].dropna().unique()
        for child in children:
            if child not in visited:
                queue.append(child)

    return accessible


def assign_user_types(df, start_menus):
    """
    Assign user types to all menu items based on which starting menus can access them.

    Args:
        df: DataFrame with menu data
        start_menus: Dict mapping starting menu names to user type names

    Returns:
        DataFrame with user_type column added
    """
    # Find all menus accessible from each starting menu
    accessibility = {}
    for start_menu, user_type in start_menus.items():
        accessible = find_accessible_menus(df, start_menu)
        accessibility[user_type] = accessible
        print(f"\n{user_type} (from {start_menu}) can access:")
        print(f"  {sorted(accessible)}")

    # Build a map of which menu items are accessible by which user types
    menu_user_types = defaultdict(set)

    for _, row in df.iterrows():
        from_menu = row['from_menu']
        to_menu = row['to_menu']

        # Check which user types can access this menu item
        for user_type, accessible_menus in accessibility.items():
            if from_menu in accessible_menus:
                # This user type can access items in this menu
                menu_user_types[(from_menu, to_menu)].add(user_type)

    # Add user_type column to DataFrame
    rows_with_types = []
    for _, row in df.iterrows():
        from_menu = row['from_menu']
        to_menu = row['to_menu']
        user_types = menu_user_types.get((from_menu, to_menu), set())

        # Create a row for each user type that can access this item
        if user_types:
            for user_type in sorted(user_types):
                new_row = row.copy()
                new_row['user_type'] = user_type
                rows_with_types.append(new_row)
        else:
            # If no user types found, add row without user_type
            new_row = row.copy()
            new_row['user_type'] = 'Unknown'
            rows_with_types.append(new_row)

    result_df = pd.DataFrame(rows_with_types)
    return result_df


# Process the data
print("="*80)
print("Inferring user types from starting menus...")
print("="*80)

df_with_users = assign_user_types(df, START_MENUS)

print("\n" + "="*80)
print("Resulting DataFrame with user types:")
print("="*80)
print(df_with_users[['from_menu', 'to_menu',
      'description', 'user_type']].to_string())

print("\n" + "="*80)
print("Statistics:")
print("="*80)
print(f"Total rows: {len(df_with_users)}")
print(f"User types: {sorted(df_with_users['user_type'].unique())}")

# Show which menus are accessible by multiple user types
print("\n" + "="*80)
print("Menus accessible by multiple user types:")
print("="*80)
multi_access = df_with_users.groupby(['from_menu', 'to_menu'])[
    'user_type'].apply(list).reset_index()
multi_access = multi_access[multi_access['user_type'].apply(len) > 1]
for _, row in multi_access.iterrows():
    to_menu = row['to_menu'] if pd.notna(row['to_menu']) else '[HEADER]'
    print(f"  {row['from_menu']} -> {to_menu}: {', '.join(row['user_type'])}")

# Now you can use this dataframe with the app
print("\n" + "="*80)
print("To use this data with the app:")
print("="*80)
print("""
from app import app

# Set the processed dataframe
app.config['df'] = df_with_users

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
""")

# Optionally run the app
if __name__ == '__main__':
    from app import app

    # Set the processed dataframe
    app.config['df'] = df_with_users

    # Set the starting menus so they appear as separate roots
    app.config['starting_menus'] = list(START_MENUS.keys())

    print("\nStarting web server on http://localhost:5000")
    print("AS/400 theme: http://localhost:5000/as400")
    print(f"\nStarting menus configured: {list(START_MENUS.keys())}")
    print("These will appear as separate root menus in the 'All Users' view")
    app.run(debug=True, port=5000)
