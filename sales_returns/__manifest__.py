{
    "name": "Sale Order Latest Quality Check",
    "version": "1.0",
    "summary": "Adds latest Quality Check info to Sale Orders",
    "depends": ["sale_management", "quality"],
    "depends": [
        "sale_management",   # for sale.order
        "stock",             # for picking_id
        "quality_control",   # for quality.check
    ],
      "installable": True,
    "application": True,   # creates its own app icon
}
