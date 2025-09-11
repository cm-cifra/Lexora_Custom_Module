# -*- coding: utf-8 -*-
{
    "name": "Custom Quality Check",
    "version": "17.0.1.0.0",
    "summary": "Display Quality Checks",
    "description": "This module displays all records from quality.check model in a menu.",
    "author": "Chris Mark Cifra", 
    "category": "Quality",
    "depends": ["stock"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/custom_quality_check_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
