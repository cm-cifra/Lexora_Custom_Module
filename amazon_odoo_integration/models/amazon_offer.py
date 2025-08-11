from odoo import models, fields

class AmazonOffer(models.Model):
    _name = 'amazon.offer'
    _description = 'Amazon Offer'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    # ... existing fields ...
