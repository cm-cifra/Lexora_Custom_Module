from odoo import models, fields

class HelpdeskApprovalWarning(models.TransientModel):
    _name = "helpdesk.approval.warning"
    _description = "Helpdesk Approval Warning"

    message = fields.Text(string="Message", readonly=True)
