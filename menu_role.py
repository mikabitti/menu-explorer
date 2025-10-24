import pandas as pd
import networkx as nx
from app import df
# # Your menu data
# df = pd.DataFrame({
#     'from_menu': ['Main', 'Main', 'Main', 'Main', 'SubMenu1', 'SubMenu2'],
#     'to_menu': ['SubMenu1', 'SubMenu1', 'SubMenu2', 'Settings', 'SubMenu3', 'Settings'],
#     'user_type': ['Admin', 'User', 'Admin', 'User', 'User2', 'Admin']
# })

# Identify starting menus (menus that appear in 'from_menu' but never in 'to_menu')
all_from = set(df['from_menu'])
all_to = set(df['to_menu'])
starting_menus = all_from - all_to

print("Starting menus:", starting_menus)

# Create a mapping of starting_menu -> user_type
# Filter rows where from_menu is a starting menu
starting_mapping = df[df['from_menu'].isin(
    starting_menus)][['from_menu', 'user_type']].drop_duplicates()

print(starting_mapping)

starting_mapping = starting_mapping.rename(
    columns={'from_menu': 'starting_menu'})

print("\nStarting menu to user_type mapping:")
print(starting_mapping)

# Build a graph to find which starting menu each node belongs to
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['from_menu'], row['to_menu'])

# For each menu, find its starting menu by traversing backwards


def find_starting_menu(menu, graph, starting_menus):
    if menu in starting_menus:
        return menu
    # Find predecessors and recursively search
    predecessors = list(graph.predecessors(menu))
    for pred in predecessors:
        result = find_starting_menu(pred, graph, starting_menus)
        if result:
            # print(f"Menu {menu} traces back to starting menu {result}")
            return result
    return None


# Add starting_menu column to original df
df['starting_menu'] = df['from_menu'].apply(
    lambda x: find_starting_menu(x, G, starting_menus))

# Merge with the mapping to get user_type
result = df.merge(starting_mapping, on='starting_menu',
                  how='left', suffixes=('_old', ''))

print("\nFinal result:")
print(result[['from_menu', 'to_menu', 'starting_menu', 'user_type']])
