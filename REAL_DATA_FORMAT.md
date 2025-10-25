# Real AS/400 Menu Data Format

## Overview

The application now supports the real AS/400 menu format with headers, descriptions, and proper ordering.

## Data Structure

### CSV Format

```
FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER;USER_TYPE
```

### Column Descriptions

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `FROM_MENU` | Yes | Parent menu identifier | `MENU1` |
| `TO_MENU` | No | Child menu or program (empty for headers) | `PROG1` or empty |
| `DESCRIPTION` | Yes | Description text | `Example desc1` |
| `MENU_ORDER` | Yes | Order of items in menu | `1`, `2`, `3` |
| `HEADER_ORDER` | Yes | Order of headers (for header rows) | `1`, `2` |
| `USER_TYPE` | Optional | User access level | `Admin`, `User` |

## Key Features

### 1. Headers and Subheaders
- Rows with **empty `TO_MENU`** are treated as headers
- Headers are displayed above their menu items
- Multiple headers can have the same `MENU_ORDER` but different `HEADER_ORDER`
- Headers appear in cyan color and uppercase

### 2. Menu Items
- Rows with a value in `TO_MENU` are menu items or submenus
- Items are ordered by `MENU_ORDER`
- Descriptions appear next to the item name in dimmed green

### 3. Ordering Logic
- Items are sorted primarily by `MENU_ORDER`
- Headers with the same `MENU_ORDER` appear before items
- Headers are sub-sorted by `HEADER_ORDER`

## Example Data

```csv
FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER;USER_TYPE
MENU1;;Header example;1;1;Admin
MENU1;PROG1;Example desc1;1;9;Admin
MENU1;PROG2;Example desc2;2;9;User
MENU1;MENU2;Example desc3;3;9;Admin
MENU1;;Subheader example;4;1;Admin
MENU1;PROG3;Example desc3;4;9;User
MENU1;PROG4;Example desc4;5;9;User
```

This creates:
```
MENU1
  HEADER EXAMPLE               <- Header (cyan)
  + PROG1 - Example desc1      <- Program item
  · PROG2 - Example desc2      <- Program item
  + MENU2 - Example desc3      <- Submenu
  SUBHEADER EXAMPLE            <- Header (cyan)
  · PROG3 - Example desc3      <- Program item
  · PROG4 - Example desc4      <- Program item
```

## Loading Your Data

### Option 1: Using load_csv_example.py

```bash
# Edit load_csv_example.py to point to your CSV file
# Then run:
uv run python load_csv_example.py
```

### Option 2: Modify app.py directly

```python
import pandas as pd

# Load your CSV
df = pd.read_csv('your_menu_data.csv', sep=';')

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Replace empty strings with None
df['to_menu'] = df['to_menu'].replace('', None)

# If no user_type column, add it:
if 'user_type' not in df.columns:
    df['user_type'] = 'Admin'
```

## UI Features

1. **Headers**: Display in cyan/yellow, bold, uppercase
2. **Descriptions**: Show dimmed next to menu item names
3. **Proper Ordering**: Items appear in MENU_ORDER sequence
4. **Collapsible Menus**: Click + to expand submenus
5. **Search**: Searches both menu names and descriptions
6. **User Filtering**: Filter by user type
7. **Path Display**: Shows full menu path when clicked

## Statistics

- **MENUS**: Count of items with children (collapsible)
- **ITEMS**: Count of leaf nodes (programs)
- **MAX DEPTH**: Maximum nesting level of current view

## Notes

- The `HEADER_ORDER` for regular menu items is typically `9` and can be ignored
- Headers never have a `TO_MENU` value
- Multiple headers can exist at the same `MENU_ORDER` level
- The application handles both old simple format and new AS/400 format automatically
