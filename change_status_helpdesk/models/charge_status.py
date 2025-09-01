from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange("x_studio_charge_status")
    def _onchange_charge_status(self):
        if self.x_studio_charge_status == "Approved":
            return {
                "warning": {
                    "title": _("Charge Status Approved"),
                    "message": _("The charge status is now set to Approved."),
                }
            }
