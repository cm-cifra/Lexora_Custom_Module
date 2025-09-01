from odoo import models, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def write(self, vals):
        res = super().write(vals)
        if 'x_studio_charge_status' in vals and vals['x_studio_charge_status'] == 'Approved':
            # Send a notification to the current user
            message = _("Charge status changed to Approved!")
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,     # recipient
                'simple_notification',        # channel
                {'title': "Information", 'message': message, 'sticky': False}
            )
        return res
