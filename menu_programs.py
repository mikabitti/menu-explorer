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


def get_test_data() -> pd.DataFrame:
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

    return df


def find_accessible_programs(df: pd.DataFrame, start_menu: str) -> set[str]:
    """
    Find all programs accessible from a starting menu.
    Uses BFS to traverse the menu tree.
    """
    leaves: set[str] = set()
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

        if len(children) == 0:
            # print(f"{current} is leaf")
            leaves.add(current)

        for child in children:
            if child not in visited:
                queue.append(child)

    return leaves


def get_unique_items(list_of_sets: list[set[str]]) -> set[str]:
    # list_of_sets = [{1, 2, 3}, {3, 4, 5}, {5, 6, 7}]
    unique_items = set()
    for s in list_of_sets:
        unique_items.update(s)
    print(unique_items)  # {1, 2, 3, 4, 5, 6, 7}
    return unique_items


if __name__ == '__main__':

    START_MENUS = ['USERMENU', 'TESTUSERMENU', 'ADMINMENU',]

    df = get_test_data()

    print(df)

    all_menus_programs: list[set] = []

    menus_programs: dict[str, set[str]] = {}

    for start_menu in START_MENUS:
        programs = find_accessible_programs(df, start_menu)
        all_menus_programs.append(programs)
        menus_programs[start_menu] = programs
        print(f"{start_menu} can access:")
        print(f"  {sorted(programs)}")

    unique_programs = get_unique_items(all_menus_programs)

    print(menus_programs)

    data = {'program': sorted(list(unique_programs))}

    prog_count = {}

    for menu in START_MENUS:
        accesslist = []
        total = 0
        print(f"Menu: {menu}")
        for uniqprog in data['program']:
            print(f"  {uniqprog}")
            if uniqprog in menus_programs[menu]:
                print(f"{uniqprog} found in {menu}")
                accesslist.append("X")
                total = total + 1
            else:
                accesslist.append("-")

        data[menu] = accesslist
        prog_count[menu] = total
        print(menu)

    df = pd.DataFrame(data)
    print(df)

    columns_to_check = START_MENUS
    df['Accessibility'] = df[columns_to_check].apply(
        lambda row: (row == 'X').sum(), axis=1)

    print(df)

    column_order = ['program', 'Accessibility']

    # for menu in START_MENUS
    print(prog_count)

    sorted_keys = sorted(prog_count, key=lambda x: prog_count[x], reverse=True)

    print(sorted_keys)

    column_order = column_order + sorted_keys

    df = df[column_order]

    print(df)
