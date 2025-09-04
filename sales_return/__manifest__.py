{
    "name": "Sale Order Returns",
    "version": "1.0",
    "summary": "Manage Sale Orders in Return States",
    "description": "Custom addon to manage sale orders in 'return_initiated' or 'returned' state",
    "category": "Sales",
    "author": "Your Name",
    "depends": ["sale"],
    'data': [
    'security/ir.model.access.csv',
    'security/sale_order_returns_security.xml',
    'views/sale_order_views.xml',
],

    "installable": True,
    "application": True,   
}
