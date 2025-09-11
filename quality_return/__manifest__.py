# -*- coding: utf-8 -*-
{
    "name": "Custom Quality Check",
    "version": "17.0.1.0.0",
    "summary": "Display Quality Checks",
    "description": "This module displays all records from quality.check model in a menu.",
    "author": "Chris Mark Cifra", 
    "category": "Quality",
    "depends": ["quality"],  # required since quality.check comes from Quality module
    "data": [
        "views/quality_check_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
