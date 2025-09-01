from odoo import models, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.onchange('tag_ids')
    def _onchange_tag_ids_show_warning(self):
        """ Show popup if 'Replacement' tag is selected """
        if self.tag_ids.filtered(lambda t: 'Replacement' in t.name):
            return {
                'warning': {
                    'title': "Replacement Tag Selected",
                    'message': "This ticket is tagged with 'Replacement'. and Po# must contain "-R" to identify as replacement Please review carefully.",
                }
            }

