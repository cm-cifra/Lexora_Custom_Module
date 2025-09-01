from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.onchange('x_studio_charge_status')
    def _onchange_charge_status(self):
        if self.x_studio_charge_status == "Approved":
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'helpdesk.approval.warning',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_message': _("Charge status is APPROVED for ticket %s.") % self.name,
                }
            }
