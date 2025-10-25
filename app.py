import pandas as pd
from flask import Flask, render_template, jsonify, request
from collections import defaultdict

app = Flask(__name__)

# Example DataFrame - replace with your actual data
# This creates a 6-level deep menu structure
df = pd.DataFrame({
    'from_menu': [
        # Level 1 -> Level 2
        'Main Menu', 'Main Menu', 'Main Menu', 'Main Menu', 'Main Menu', 'Main Menu',

        # Level 2 -> Level 3 (Financial Management)
        'Financial Management', 'Financial Management', 'Financial Management', 'Financial Management',

        # Level 2 -> Level 3 (Human Resources)
        'Human Resources', 'Human Resources', 'Human Resources', 'Human Resources',

        # Level 2 -> Level 3 (Inventory Control)
        'Inventory Control', 'Inventory Control', 'Inventory Control', 'Inventory Control',

        # Level 2 -> Level 3 (Sales & Orders)
        'Sales & Orders', 'Sales & Orders', 'Sales & Orders',

        # Level 2 -> Level 3 (Reports)
        'Reports', 'Reports', 'Reports', 'Reports',

        # Level 3 -> Level 4 (Accounts Payable)
        'Accounts Payable', 'Accounts Payable', 'Accounts Payable', 'Accounts Payable',

        # Level 3 -> Level 4 (Accounts Receivable)
        'Accounts Receivable', 'Accounts Receivable', 'Accounts Receivable',

        # Level 3 -> Level 4 (General Ledger)
        'General Ledger', 'General Ledger', 'General Ledger', 'General Ledger',

        # Level 3 -> Level 4 (Payroll Processing)
        'Payroll Processing', 'Payroll Processing', 'Payroll Processing', 'Payroll Processing',

        # Level 3 -> Level 4 (Employee Management)
        'Employee Management', 'Employee Management', 'Employee Management',

        # Level 3 -> Level 4 (Warehouse Operations)
        'Warehouse Operations', 'Warehouse Operations', 'Warehouse Operations',

        # Level 3 -> Level 4 (Purchase Orders)
        'Purchase Orders', 'Purchase Orders', 'Purchase Orders',

        # Level 3 -> Level 4 (Order Processing)
        'Order Processing', 'Order Processing', 'Order Processing', 'Order Processing',

        # Level 4 -> Level 5 (Invoice Management)
        'Invoice Management', 'Invoice Management', 'Invoice Management',

        # Level 4 -> Level 5 (Vendor Management)
        'Vendor Management', 'Vendor Management', 'Vendor Management',

        # Level 4 -> Level 5 (Payment Processing)
        'Payment Processing', 'Payment Processing', 'Payment Processing',

        # Level 4 -> Level 5 (Customer Invoices)
        'Customer Invoices', 'Customer Invoices', 'Customer Invoices',

        # Level 4 -> Level 5 (Collections)
        'Collections', 'Collections', 'Collections',

        # Level 4 -> Level 5 (Journal Entries)
        'Journal Entries', 'Journal Entries', 'Journal Entries',

        # Level 4 -> Level 5 (Chart of Accounts)
        'Chart of Accounts', 'Chart of Accounts', 'Chart of Accounts',

        # Level 4 -> Level 5 (Time Entry)
        'Time Entry', 'Time Entry', 'Time Entry',

        # Level 4 -> Level 5 (Payroll Reports)
        'Payroll Reports', 'Payroll Reports', 'Payroll Reports',

        # Level 4 -> Level 5 (Employee Records)
        'Employee Records', 'Employee Records', 'Employee Records',

        # Level 4 -> Level 5 (Receiving)
        'Receiving', 'Receiving', 'Receiving',

        # Level 4 -> Level 5 (Shipping)
        'Shipping', 'Shipping', 'Shipping',

        # Level 4 -> Level 5 (Order Entry)
        'Order Entry', 'Order Entry', 'Order Entry',

        # Level 5 -> Level 6 (Create Invoice)
        'Create Invoice', 'Create Invoice',

        # Level 5 -> Level 6 (Edit Invoice)
        'Edit Invoice', 'Edit Invoice',

        # Level 5 -> Level 6 (Add Vendor)
        'Add Vendor', 'Add Vendor',

        # Level 5 -> Level 6 (Edit Vendor)
        'Edit Vendor', 'Edit Vendor',

        # Level 5 -> Level 6 (Process Payment)
        'Process Payment', 'Process Payment',

        # Level 5 -> Level 6 (Payment History)
        'Payment History', 'Payment History',

        # Level 5 -> Level 6 (View Employee)
        'View Employee', 'View Employee',

        # Level 5 -> Level 6 (Edit Employee)
        'Edit Employee', 'Edit Employee',

        # Level 5 -> Level 6 (Receive Goods)
        'Receive Goods', 'Receive Goods',

        # Level 5 -> Level 6 (Ship Order)
        'Ship Order', 'Ship Order',
    ],
    'to_menu': [
        # Level 1 -> Level 2
        'Financial Management', 'Human Resources', 'Inventory Control', 'Sales & Orders',
        'Reports', 'System Settings',

        # Level 2 -> Level 3 (Financial Management)
        'Accounts Payable', 'Accounts Receivable', 'General Ledger', 'Banking',

        # Level 2 -> Level 3 (Human Resources)
        'Payroll Processing', 'Employee Management', 'Benefits Administration', 'Time & Attendance',

        # Level 2 -> Level 3 (Inventory Control)
        'Warehouse Operations', 'Stock Management', 'Purchase Orders', 'Physical Inventory',

        # Level 2 -> Level 3 (Sales & Orders)
        'Order Processing', 'Customer Management', 'Pricing',

        # Level 2 -> Level 3 (Reports)
        'Financial Reports', 'Operational Reports', 'Custom Reports', 'Scheduled Reports',

        # Level 3 -> Level 4 (Accounts Payable)
        'Invoice Management', 'Vendor Management', 'Payment Processing', '1099 Processing',

        # Level 3 -> Level 4 (Accounts Receivable)
        'Customer Invoices', 'Collections', 'Credit Management',

        # Level 3 -> Level 4 (General Ledger)
        'Journal Entries', 'Chart of Accounts', 'Period Close', 'Budget Management',

        # Level 3 -> Level 4 (Payroll Processing)
        'Time Entry', 'Payroll Reports', 'Tax Processing', 'Direct Deposit',

        # Level 3 -> Level 4 (Employee Management)
        'Employee Records', 'Hiring & Onboarding', 'Performance Reviews',

        # Level 3 -> Level 4 (Warehouse Operations)
        'Receiving', 'Shipping', 'Bin Management',

        # Level 3 -> Level 4 (Purchase Orders)
        'Create PO', 'Approve PO', 'PO History',

        # Level 3 -> Level 4 (Order Processing)
        'Order Entry', 'Order Status', 'Backorders', 'Returns',

        # Level 4 -> Level 5 (Invoice Management)
        'Create Invoice', 'Edit Invoice', 'Delete Invoice',

        # Level 4 -> Level 5 (Vendor Management)
        'Add Vendor', 'Edit Vendor', 'Vendor Reports',

        # Level 4 -> Level 5 (Payment Processing)
        'Process Payment', 'Payment History', 'Void Payment',

        # Level 4 -> Level 5 (Customer Invoices)
        'Generate Invoice', 'View Invoices', 'Apply Credits',

        # Level 4 -> Level 5 (Collections)
        'Aging Report', 'Send Notices', 'Payment Plans',

        # Level 4 -> Level 5 (Journal Entries)
        'Manual Entry', 'Recurring Entries', 'Entry History',

        # Level 4 -> Level 5 (Chart of Accounts)
        'View Accounts', 'Add Account', 'Edit Account',

        # Level 4 -> Level 5 (Time Entry)
        'Enter Time', 'Approve Time', 'Time Reports',

        # Level 4 -> Level 5 (Payroll Reports)
        'Pay Stub', 'Tax Summary', 'Deductions',

        # Level 4 -> Level 5 (Employee Records)
        'View Employee', 'Edit Employee', 'Terminate Employee',

        # Level 4 -> Level 5 (Receiving)
        'Receive Goods', 'Receive Against PO', 'Receiving History',

        # Level 4 -> Level 5 (Shipping)
        'Ship Order', 'Print Labels', 'Shipping History',

        # Level 4 -> Level 5 (Order Entry)
        'New Order', 'Quick Order', 'Import Orders',

        # Level 5 -> Level 6 (Create Invoice)
        'Standard Invoice', 'Recurring Invoice',

        # Level 5 -> Level 6 (Edit Invoice)
        'Edit Header', 'Edit Line Items',

        # Level 5 -> Level 6 (Add Vendor)
        'Domestic Vendor', 'International Vendor',

        # Level 5 -> Level 6 (Edit Vendor)
        'Edit Details', 'Edit Terms',

        # Level 5 -> Level 6 (Process Payment)
        'Check Payment', 'ACH Payment',

        # Level 5 -> Level 6 (Payment History)
        'View All', 'By Vendor',

        # Level 5 -> Level 6 (View Employee)
        'Personal Info', 'Employment History',

        # Level 5 -> Level 6 (Edit Employee)
        'Edit Personal', 'Edit Compensation',

        # Level 5 -> Level 6 (Receive Goods)
        'Full Receipt', 'Partial Receipt',

        # Level 5 -> Level 6 (Ship Order)
        'Full Shipment', 'Partial Shipment',
    ],
    'user_type': [
        # Level 1 -> Level 2
        'Admin', 'Admin', 'Admin', 'User', 'User', 'Admin',

        # Financial Management paths
        'Admin', 'User', 'Admin', 'Admin',

        # Human Resources paths
        'HR Manager', 'HR Manager', 'HR Manager', 'Manager',

        # Inventory Control paths
        'Warehouse Manager', 'Warehouse Clerk', 'Buyer', 'Warehouse Manager',

        # Sales & Orders paths
        'Sales Rep', 'Sales Manager', 'Admin',

        # Reports paths
        'Admin', 'Manager', 'User', 'Admin',

        # Accounts Payable paths
        'AP Clerk', 'AP Clerk', 'AP Manager', 'Admin',

        # Accounts Receivable paths
        'AR Clerk', 'AR Manager', 'AR Manager',

        # General Ledger paths
        'Accountant', 'Admin', 'Controller', 'Controller',

        # Payroll paths
        'HR Clerk', 'HR Manager', 'Payroll Admin', 'Payroll Admin',

        # Employee Management paths
        'HR Clerk', 'HR Manager', 'Manager',

        # Warehouse Operations paths
        'Warehouse Clerk', 'Warehouse Clerk', 'Warehouse Manager',

        # Purchase Orders paths
        'Buyer', 'Buyer Manager', 'Buyer',

        # Order Processing paths
        'Sales Rep', 'Sales Rep', 'Sales Manager', 'Sales Rep',

        # Invoice Management (Level 5)
        'AP Clerk', 'AP Clerk', 'AP Manager',

        # Vendor Management (Level 5)
        'AP Clerk', 'AP Clerk', 'AP Manager',

        # Payment Processing (Level 5)
        'AP Manager', 'AP Clerk', 'AP Manager',

        # Customer Invoices (Level 5)
        'AR Clerk', 'AR Clerk', 'AR Clerk',

        # Collections (Level 5)
        'AR Manager', 'AR Manager', 'AR Manager',

        # Journal Entries (Level 5)
        'Accountant', 'Controller', 'Accountant',

        # Chart of Accounts (Level 5)
        'Accountant', 'Controller', 'Controller',

        # Time Entry (Level 5)
        'User', 'Manager', 'HR Manager',

        # Payroll Reports (Level 5)
        'User', 'Manager', 'Payroll Admin',

        # Employee Records (Level 5)
        'HR Clerk', 'HR Manager', 'HR Manager',

        # Receiving (Level 5)
        'Warehouse Clerk', 'Warehouse Clerk', 'Warehouse Clerk',

        # Shipping (Level 5)
        'Warehouse Clerk', 'Warehouse Clerk', 'Warehouse Clerk',

        # Order Entry (Level 5)
        'Sales Rep', 'Sales Rep', 'Admin',

        # Level 6 paths
        'AP Clerk', 'AP Clerk',  # Create Invoice
        'AP Clerk', 'AP Manager',  # Edit Invoice
        'AP Clerk', 'Admin',  # Add Vendor
        'AP Clerk', 'AP Manager',  # Edit Vendor
        'AP Manager', 'Payroll Admin',  # Process Payment
        'AP Clerk', 'AP Manager',  # Payment History
        'HR Clerk', 'Manager',  # View Employee
        'HR Manager', 'Admin',  # Edit Employee
        'Warehouse Clerk', 'Warehouse Manager',  # Receive Goods
        'Warehouse Clerk', 'Warehouse Manager',  # Ship Order
    ]
})


def build_tree(dataframe, user_type_filter=None):
    """Build a hierarchical tree structure from the DataFrame."""
    # Filter by user type if specified
    if user_type_filter and user_type_filter != 'All':
        dataframe = dataframe[dataframe['user_type'] == user_type_filter]

    # Check if we have the new format with description and ordering
    has_description = 'description' in dataframe.columns
    has_ordering = 'menu_order' in dataframe.columns and 'header_order' in dataframe.columns

    # Build adjacency list
    tree_dict = defaultdict(lambda: {
        'children': [],
        'user_types': set(),
        'headers': []
    })
    all_nodes = set()
    child_nodes = set()

    for _, row in dataframe.iterrows():
        from_menu = row['from_menu']
        to_menu = row['to_menu'] if pd.notna(row['to_menu']) and row['to_menu'] else None
        user_type = row.get('user_type', '')

        all_nodes.add(from_menu)

        # Handle headers (when to_menu is empty)
        if not to_menu:
            if has_description:
                header_info = {
                    'text': row.get('description', ''),
                    'menu_order': row.get('menu_order', 0) if has_ordering else 0,
                    'header_order': row.get('header_order', 0) if has_ordering else 0
                }
                tree_dict[from_menu]['headers'].append(header_info)
        else:
            # Handle regular menu items
            all_nodes.add(to_menu)
            child_nodes.add(to_menu)

            child_info = {
                'name': to_menu,
                'description': row.get('description', '') if has_description else '',
                'menu_order': row.get('menu_order', 0) if has_ordering else 0,
                'user_type': user_type
            }

            tree_dict[from_menu]['children'].append(child_info)
            tree_dict[from_menu]['user_types'].add(user_type)
            tree_dict[to_menu]['user_types'].add(user_type)

    # Find root nodes (nodes that are not children of any other node)
    root_nodes = all_nodes - child_nodes

    def build_node(node_name, visited=None):
        """Recursively build tree structure."""
        if visited is None:
            visited = set()

        if node_name in visited:
            return None

        visited.add(node_name)

        node = {
            'name': node_name,
            'user_types': sorted(list(tree_dict[node_name]['user_types'])),
            'headers': sorted(tree_dict[node_name]['headers'],
                            key=lambda x: (x.get('menu_order', 0), x.get('header_order', 0))),
            'children': []
        }

        # Sort children by menu_order
        sorted_children = sorted(tree_dict[node_name]['children'],
                                key=lambda x: x.get('menu_order', 0))

        for child_info in sorted_children:
            child_name = child_info['name']
            child_node = build_node(child_name, visited.copy())
            if child_node:
                # Add description to the child node
                child_node['description'] = child_info.get('description', '')
                child_node['menu_order'] = child_info.get('menu_order', 0)
                node['children'].append(child_node)

        return node

    # Build tree for each root
    tree = []
    for root in sorted(root_nodes):
        root_node = build_node(root)
        if root_node:
            tree.append(root_node)

    return tree


@app.route('/')
def index():
    """Render the main page."""
    data = app.config.get('df', df)
    user_types = sorted(data['user_type'].unique().tolist()) if 'user_type' in data.columns else ['Admin']
    return render_template('index.html', user_types=user_types)


@app.route('/as400')
def as400_theme():
    """Render the AS/400 themed page."""
    data = app.config.get('df', df)
    user_types = sorted(data['user_type'].unique().tolist()) if 'user_type' in data.columns else ['Admin']
    return render_template('as400.html', user_types=user_types)


@app.route('/api/tree')
def get_tree():
    """API endpoint to get the tree structure."""
    user_type = request.args.get('user_type', 'All')
    search = request.args.get('search', '').strip().lower()

    # Use custom dataframe if provided in app config, otherwise use default
    data = app.config.get('df', df)

    tree = build_tree(data, user_type if user_type != 'All' else None)

    # Filter tree by search if provided
    if search:
        tree = filter_tree_by_search(tree, search)

    return jsonify(tree)


def filter_tree_by_search(tree, search_term):
    """Filter tree to only show nodes matching the search term."""
    filtered_tree = []

    for node in tree:
        filtered_node = filter_node(node, search_term)
        if filtered_node:
            filtered_tree.append(filtered_node)

    return filtered_tree


def filter_node(node, search_term):
    """Recursively filter a node and its children."""
    # Check if current node matches (search in name and description)
    node_matches = search_term in node['name'].lower()

    # Also search in description if available
    if not node_matches and 'description' in node and node['description']:
        node_matches = search_term in node['description'].lower()

    # Search in headers if available
    header_matches = False
    if not node_matches and 'headers' in node and node['headers']:
        for header in node['headers']:
            if search_term in header.get('text', '').lower():
                header_matches = True
                break

    # Recursively filter children
    filtered_children = []
    for child in node.get('children', []):
        filtered_child = filter_node(child, search_term)
        if filtered_child:
            filtered_children.append(filtered_child)

    # Keep node if it matches or has matching children
    if node_matches or header_matches or filtered_children:
        return {
            'name': node['name'],
            'user_types': node['user_types'],
            'description': node.get('description', ''),
            'menu_order': node.get('menu_order', 0),
            'headers': node.get('headers', []),
            'children': filtered_children,
            'highlighted': node_matches or header_matches
        }

    return None


if __name__ == '__main__':
    app.run(debug=True, port=5000)
