{
"name": "return report",
"version": "1.0",
"summary": "Custom records with PO number, product SKU, carrier and shipment/return metadata",
"description": "",
"author": "chris mark cifra",
"category": "Sales",
"depends": ["sale_management", "product"],
"data": [
"security/security.xml",
"security/ir.model.access.csv",
"views/custom_record_views.xml",
],
"installable": True,
"application": False,
"auto_install": False,
}