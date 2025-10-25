# Menu Explorer

A web-based hierarchical menu visualization tool for exploring menu structures from AS/400 systems.

## Features

- **Interactive Tree View**: Collapsible/expandable hierarchical menu structure
- **Search Functionality**: Search for specific menu items across the entire tree
- **User Type Filtering**: Filter menus by user type (Admin, User, etc.)
- **Highlighted Search Results**: Matching items are highlighted in the tree
- **Statistics Dashboard**: View total menu counts and visible nodes
- **Responsive Design**: Clean, modern UI that works on different screen sizes

## Installation

1. Install dependencies:
```bash
uv sync
```

## Usage

### 1. Prepare Your Data

The application supports two data formats:

#### Simple Format (for testing):
```python
df = pd.DataFrame({
    'from_menu': ['Main', 'Main', 'Main'],
    'to_menu': ['SubMenu1', 'SubMenu2', 'Settings'],
    'user_type': ['Admin', 'User', 'Admin']
})
```

#### Real AS/400 Format (with headers and descriptions):
Your CSV file should have these columns:
- `FROM_MENU`: Parent menu name
- `TO_MENU`: Child menu/program name (empty for headers)
- `DESCRIPTION`: Description of the menu item
- `MENU_ORDER`: Order number for items in the menu
- `HEADER_ORDER`: Order number for headers (when TO_MENU is empty)
- `USER_TYPE`: User type that can access this item (optional)

Example CSV:
```
FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER;USER_TYPE
MENU1;;Header example;1;1;Admin
MENU1;PROG1;Example desc1;1;9;Admin
MENU1;PROG2;Example desc2;2;9;User
MENU1;;Subheader example;4;1;Admin
MENU1;PROG3;Example desc3;4;9;User
```

**Loading from CSV**:
```python
# See load_csv_example.py for a complete example
import pandas as pd
df = pd.read_csv('your_menu_data.csv', sep=';')
df.columns = df.columns.str.strip().str.lower()
df['to_menu'] = df['to_menu'].replace('', None)
```

### 2. Run the Application

```bash
uv run python app.py
```

The application will start on http://localhost:5000

### 3. Using the Interface

- **Search**: Type in the search box and click "Apply Filters" or press Enter
- **Filter by User Type**: Select a user type from the dropdown and click "Apply Filters"
- **Expand/Collapse**: Click the arrow next to each menu item to expand/collapse children
- **Expand/Collapse All**: Use the button in the top right to expand or collapse all nodes at once

## Loading Data from AS/400

To load data from your AS/400 system, you can:

1. Export menu data to CSV format
2. Load it in [app.py](app.py) using pandas:

```python
df = pd.read_csv('menu_data.csv')
```

Or connect directly to AS/400 using appropriate Python libraries (pyodbc, ibm_db, etc.).

## Project Structure

```
menu-explorer/
 app.py                  # Flask application and tree-building logic
 templates/
    index.html          # Web interface
 main.py                # Example data script
 pyproject.toml         # Project dependencies
 README.md              # This file
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas
