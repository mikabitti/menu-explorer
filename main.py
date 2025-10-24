
import pandas as pd


# Example DataFrame of menu relationships
df = pd.DataFrame({
    'from_menu': ['Main', 'Main', 'Main', 'Main', 'SubMenu1', 'SubMenu2'],
    'to_menu': ['SubMenu1', 'SubMenu1', 'SubMenu2', 'Settings', 'SubMenu3', 'Settings'],
    'user_type': ['Admin', 'User', 'Admin', 'User', 'User2', 'Admin']
})
print(df)
