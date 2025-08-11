from odoo import models, fields, api

class AmazonOffer(models.Model):
    _name = 'amazon.offer'
    _description = 'Amazon Offer'

    # Add this missing field
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    # ... keep your other fields here ...
