from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange("x_studio_charge_status")
    def _onchange_charge_status(self):
        if self.x_studio_charge_status == "disputed":
            return {
                "warning": {
                    "title": _("Are you sure?"),
                    "message": _("You are marking this ticket as DISPUTED. Please confirm this action."),
                }
            }
