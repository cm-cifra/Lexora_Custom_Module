from odoo import models, api, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def action_check_charge_status(self):
        for rec in self:
            if rec.x_studio_charge_status == 'approved':
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
