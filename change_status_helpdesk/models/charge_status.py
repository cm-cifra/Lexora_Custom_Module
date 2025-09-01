from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.onchange('x_studio_charge_status')
    def _onchange_charge_status(self):
        """
        Option 1: Show yellow banner warning immediately when status changes to Approved.
        """
        if self.x_studio_charge_status == "Approved":  # case-sensitive
            return {
                'warning': {
                    'title': _("Charge Status Approved"),
                    'message': _("This ticket's charge status is set to APPROVED! Please review carefully."),
                }
            }

    def action_check_charge_status(self):
        """
        Option 2: Show modal popup wizard if charge status == Approved.
        Triggered by a button in form view.
        """
        for rec in self:
            if rec.x_studio_charge_status == "Approved":
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'helpdesk.approval.warning',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_message': _("Charge status is APPROVED for ticket %s.") % rec.name,
                    }
                }
        return True
