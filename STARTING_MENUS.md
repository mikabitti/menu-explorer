# Starting Menus and User Type Inference

## Overview

In AS/400 systems, users are assigned **starting menus** (like `ADMINMENU`, `USERMENU`). These starting menus determine what programs and submenus a user can access.

The `load_csv_with_user_inference.py` script automatically determines which user types can access each menu item based on which starting menus can reach them.

## How It Works

### Example Data

```csv
FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER
ADMINMENU;ADMPROG1;Admin Program 1;1;9
ADMINMENU;USERMENU;User Menu Access;2;9
USERMENU;PROG1;Program 1;1;9
USERMENU;PROG2;Program 2;2;9
```

### Starting Menu Configuration

```python
START_MENUS = {
    'ADMINMENU': 'Admin',    # Admin users start at ADMINMENU
    'USERMENU': 'User'       # Regular users start at USERMENU
}
```

### Accessibility Tree

The script uses BFS (Breadth-First Search) to find all reachable menus:

```
ADMINMENU
├── ADMPROG1 (Admin only)
├── ADMPROG2 (Admin only)
└── USERMENU (Admin can access this)
    ├── PROG1 (Both Admin and User)
    ├── PROG2 (Both Admin and User)
    └── USERMENU2 (Both Admin and User)
        ├── PROG3 (Both Admin and User)
        └── PROG4 (Both Admin and User)

USERMENU
├── PROG1 (User and Admin)
├── PROG2 (User and Admin)
└── USERMENU2 (User and Admin)
    ├── PROG3 (User and Admin)
    └── PROG4 (User and Admin)
```

## Result

The script creates duplicate rows for items accessible by multiple user types:

| FROM_MENU | TO_MENU | DESCRIPTION | USER_TYPE |
|-----------|---------|-------------|-----------|
| ADMINMENU | ADMPROG1 | Admin Program 1 | Admin |
| ADMINMENU | USERMENU | User Menu Access | Admin |
| USERMENU | PROG1 | Program 1 | Admin |
| USERMENU | PROG1 | Program 1 | User |
| USERMENU | PROG2 | Program 2 | Admin |
| USERMENU | PROG2 | Program 2 | User |

## Usage

### 1. Prepare Your Data

Create a CSV file with your menu structure (no USER_TYPE column needed):

```csv
FROM_MENU;TO_MENU;DESCRIPTION;MENU_ORDER;HEADER_ORDER
ADMINMENU;;Administration;1;1
ADMINMENU;SYSPROG;System Programs;1;9
ADMINMENU;USERMENU;User Functions;2;9
USERMENU;;User Menu;1;1
USERMENU;PROG1;Program 1;1;9
```

### 2. Define Starting Menus

Edit `load_csv_with_user_inference.py`:

```python
START_MENUS = {
    'ADMINMENU': 'Admin',
    'MANAGERMENU': 'Manager',
    'USERMENU': 'User',
    'CLERKMENU': 'Clerk'
}
```

### 3. Run the Script

```bash
uv run python load_csv_with_user_inference.py
```

This will:
1. Load your CSV data
2. Traverse the menu tree from each starting menu
3. Tag all reachable items with the appropriate user type(s)
4. Start the web application with the processed data

## Benefits

✅ **Automatic user type assignment** - No need to manually tag every menu item

✅ **Handles inheritance** - Automatically tags shared menus with all user types that can reach them

✅ **Realistic permissions** - Reflects actual AS/400 access patterns

✅ **Easy to maintain** - Just update starting menus, not every individual item

## Web Interface

Once loaded, you can:
- **Filter by user type** to see what each role can access
- **Search** across all accessible programs
- **View inheritance** - See which programs are tagged with multiple user types

### Starting Menus as Roots

The script automatically configures starting menus as separate root nodes in the tree, even if they're submenus of each other.

For example:
- **ADMINMENU** can access **USERMENU** as a submenu
- But when viewing **"All Users"**, both appear as separate roots:
  ```
  + ADMINMENU
  + USERMENU
  ```

This makes it easy to see each user role's starting point in the menu structure.

## Example Output

When you filter by user type in the web interface:

**Admin View:**
- Shows ADMPROG1, ADMPROG2, ADMPROG3 (admin-only programs)
- Shows PROG1, PROG2, PROG3, PROG4 (inherited from USERMENU)

**User View:**
- Shows PROG1, PROG2, PROG3, PROG4 (their programs)
- Does NOT show ADMPROG1, ADMPROG2, ADMPROG3 (admin-only)

## Multiple User Types Badge

Programs accessible by multiple user types will show multiple badges:

```
PROG1 - Program 1  [Admin] [User]
```

This makes it easy to see which programs are shared vs. restricted.
