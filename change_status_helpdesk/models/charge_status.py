from odoo import models, api
from odoo.exceptions import UserError

DISPUTED_VALUE = "Disputed"  # the exact value your selection uses

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange('x_studio_charge_status')
    def _onchange_x_studio_charge_status_warning(self):
        """Optional: show a warning banner at selection time."""
        if self.x_studio_charge_status == DISPUTED_VALUE:
            return {
                "warning": {
                    "title": "Confirmation required",
                    "message": (
                        "You selected 'Disputed'. This action requires confirmation. "
                        "Please use the 'Mark as Disputed' button in the header."
                    ),
                }
            }

    def write(self, vals):
        """
        Enforce confirmation: block direct writes to 'Disputed' unless the wizard set a context flag.
        """
        if 'x_studio_charge_status' in vals and vals['x_studio_charge_status'] == DISPUTED_VALUE:
            if not self.env.context.get('confirm_disputed'):
                # Block direct setting and instruct user to use the button
                raise UserError(
                    "Setting 'Charge Status' to 'Disputed' requires confirmation.\n\n"
                    "Please click the 'Mark as Disputed' button in the header."
                )
        return super().write(vals)

    def action_open_dispute_confirm_wizard(self):
        """Open the Yes/No confirmation wizard."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Confirm Dispute",
            "res_model": "dispute.confirm.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_model": self._name,
                "active_id": self.id,
            },
        }

    def action_unset_disputed(self):
        """Optional helper: clear the 'Disputed' status without confirmation."""
        for rec in self:
            if rec.x_studio_charge_status == DISPUTED_VALUE:
                rec.with_context(confirm_disputed=True).write({"x_studio_charge_status": False})
        return True
