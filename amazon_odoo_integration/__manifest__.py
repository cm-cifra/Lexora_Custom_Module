{
    "name": "Amazon Connector (starter)",
    "version": "1.0.0",
    "summary": "Sync Amazon Products and Sales Orders by account name and marketplace",
    "author": "You / Your Company",
    "depends": ["sale", "product", "base"],   
    "data": [
        "security/ir.model.access.csv",
        "views/amazon_account_views.xml",
        "views/amazon_mapping_views.xml",
        "data/cron_data.xml",
    ],
    "installable": True,
    "application": False,
}
