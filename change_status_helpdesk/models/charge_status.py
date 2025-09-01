from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def write(self, vals):
        res = super().write(vals)

        for record in self:
            if 'x_studio_charge_status' in vals and vals['x_studio_charge_status'] == 'approved':
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'helpdesk.approval.warning',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_message': _("Charge status has been approved for ticket: %s. Please review carefully.") % record.name,
                    }
                }

        return res
