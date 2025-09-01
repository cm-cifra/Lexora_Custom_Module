from odoo import models

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def write(self, vals):
        res = super().write(vals)
        if 'x_studio_charge_status' in vals and vals['x_studio_charge_status'] == 'Approved':
            self.env.user.notify_info(
                message="Charge status changed to Approved!",
                title="Information"
            )
        return res
