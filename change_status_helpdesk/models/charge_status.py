from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange("x_studio_charge_status")
    def _onchange_charge_status_warning(self):
        """Show an immediate yellow warning banner when the field becomes 'Approved'."""
        if self.x_studio_charge_status == "Approved":  # case-sensitive
            return {
                "warning": {
                    "title": _("Charge Status Approved"),
                    "message": _(
                        "This ticket's charge status is set to APPROVED. Please review carefully."
                    ),
                }
            }

    def action_check_charge_status(self):
        """Open a modal popup wizard if the field is 'Approved'."""
        self.ensure_one()
        if self.x_studio_charge_status == "Approved":
            return {
                "type": "ir.actions.act_window",
                "res_model": "helpdesk.approval.warning",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_message": _(
                        "Charge status is APPROVED for ticket %s."
                    ) % (self.display_name or self.name),
                },
            }
        # Nothing to show
        return True
