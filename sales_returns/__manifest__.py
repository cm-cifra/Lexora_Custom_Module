{
    "name": "Sale Order Latest Quality Check",
    "version": "17.0.1.0.0",
    "summary": "Adds latest Quality Check info to Sale Orders",
    "depends": ["sale_management", "quality"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
