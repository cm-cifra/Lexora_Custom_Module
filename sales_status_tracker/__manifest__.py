{
    'name': 'Sales Order Tracking Report',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'View all sales orders with delivery details',
    'description': 'Custom list view showing sales orders with carrier, delivery date, and expected delivery date',
    'author': 'Your Name',
    'depends': ['sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/order_tracking_view.xml',
    ],
    'installable': True,
    'application': False,
}
