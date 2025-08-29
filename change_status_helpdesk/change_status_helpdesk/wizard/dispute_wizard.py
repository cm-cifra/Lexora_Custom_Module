# models/dispute_confirm_wizard.py
from odoo import models, fields

class DisputeConfirmWizard(models.TransientModel):
    _name = "dispute.confirm.wizard"
    _description = "Dispute Confirmation Wizard"

    ticket_id = fields.Many2one("helpdesk.ticket", required=True)

    def action_confirm(self):
        """User confirmed 'Disputed'"""
        self.ticket_id.x_studio_charge_status = "Disputed"
        return {"type": "ir.actions.act_window_close"}

    def action_cancel(self):
        """User canceled -> reset field"""
        self.ticket_id.x_studio_charge_status = False
        return {"type": "ir.actions.act_window_close"}
