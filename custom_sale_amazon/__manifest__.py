# __manifest__.py
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Custom Amazon Connector",
    "summary": "Import Amazon orders and sync deliveries",
    "description": """
Import your Amazon orders in Odoo and synchronize deliveries
============================================================

Key Features
------------
* Import orders from multiple accounts and marketplaces.
* Orders are matched with Odoo products based on their internal reference (Amazon SKU).
* Deliveries confirmed in Odoo are synchronized with Amazon.
* Supports FBA and FBM:
  * FBA: Monitor Amazon FC stock via location & stock moves.
  * FBM: Send delivery notifications to Amazon for each confirmed picking (partial delivery friendly).
""",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "sequence": 320,
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OEEL-1",  # keep your original license; change to "LGPL-3" if you prefer
    "website": "https://your-company.example.com",
    "author": "Your Company",
    "maintainer": "Your Company",
    "depends": [
        "sale_management",
        "stock","sale_amazon",
        "delivery",  # modern module for carriers/shipments
        # add "mail" if you rely on templates or chatter features
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/sale_amazon_security.xml",
        "data/amazon_data.xml",
        "data/amazon_cron.xml",
        "data/mail_template_data.xml",
        "views/amazon_account_views.xml",
        "views/amazon_marketplace_views.xml",
        "views/amazon_offer_views.xml",
        "views/amazon_templates.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "wizards/recover_order_wizard_views.xml",
    ],
    # Optional if you have kanban images or screenshots for the Apps view
    "images": [
        "static/description/icon.png",
        "static/description/icon.svg",
        # "static/description/screenshot_01.png",
    ],
    # Only add assets if you actually ship JS/CSS/QWeb files
    # "assets": {
    #     "web.assets_backend": [
    #         "custom_amazon_connector/static/src/**/*",
    #     ],
    #     "web.assets_qweb": [
    #         "custom_amazon_connector/static/src/xml/**/*.xml",
    #     ],
    # },
}
