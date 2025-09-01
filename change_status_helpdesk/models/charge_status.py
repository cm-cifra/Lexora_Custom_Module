from odoo import models, api, _
from odoo.exceptions import UserError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.onchange('x_studio_charge_status')
    def _onchange_charge_status(self):
        if self.x_studio_charge_status == 'Approved':
            # Blocking popup
            return {
                'warning': {
                    'title': _("Information"),
                    'message': _("⚠️ The charge status has been set to Approved!"),
                }
            }
