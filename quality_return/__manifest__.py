# -*- coding: utf-8 -*-
{
    "name": "Custom Quality Check",
    "version": "17.0.1.0.0",
    "summary": "Custom model showing Quality Checks",
    "description": "This module creates a new model and fetches data from quality.check",
    "author": "chris mark cifra", 
    "category": "Quality",
    "depends": ["quality"],  # depends on Quality app
    "data": [
        "security/ir.model.access.csv",
        "views/custom_quality_check_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
