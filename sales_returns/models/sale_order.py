from odoo import models, fields

class QualityCheck(models.Model):
    _inherit = "quality.check"

    sale_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        related="picking_id.sale_id",
        store=True,
        readonly=True,
    )
