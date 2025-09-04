{
    "name": "Return Reports",
    "version": "1.0",
    "summary": "Custom Return Report Application",
    "category": "Reporting",
    "author": "chris",
    
    'depends': ['base', 'sale', 'mail'],  # <-- add 'mail' here
    "data": [
        "security/ir.model.access.csv",
        "views/return_report_views.xml",
    ],
    "application": True,
    "installable": True,
}
