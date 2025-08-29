# models/helpdesk_ticket.py
from odoo import models

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def write(self, vals):
        if vals.get("x_studio_charge_status") == "Disputed":
            # Intercept and open wizard
            return {
                "name": "Confirm Dispute",
                "type": "ir.actions.act_window",
                "res_model": "dispute.confirm.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_ticket_id": self.id,
                },
            }
        return super().write(vals)
