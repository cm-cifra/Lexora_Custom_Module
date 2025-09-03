{
    "name": "Return Report",
    "version": "1.0",
    "author": "Chris Mark Cifra",
    "category": "Sales",
    "summary": "Manage product returns linked to Sales Orders",
    "depends": ["sale_management", "product", "delivery"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/custom_record_views.xml",
    ],
    "installable": True,
    "application": True,
}
