{
    'name': 'Amazon Product Mapper',
    'version': '1.0',
    'summary': 'Ensure Amazon products match Odoo products by SKU or Barcode',
    'description': 'Checks and enforces mappings between Amazon and Odoo products using SKU or Barcode.',
    'category': 'Inventory',
    'author': 'chris',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/amazon_product_views.xml',
    ],
    'installable': True,
    'application': False,
}
