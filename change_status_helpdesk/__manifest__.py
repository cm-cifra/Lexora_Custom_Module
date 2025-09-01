{
    'name': 'Helpdesk Ticket Alert',
    'version': '1.0',
    'summary': 'Show alert when charge status changes to Approved',
    'description': """
        This module adds an alert message when the field 
        x_studio_charge_status in helpdesk.ticket is changed to "Approved".
    """,
    'category': 'Helpdesk',
    'author': 'chris mark cifra',
    'depends': ['helpdesk'],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
