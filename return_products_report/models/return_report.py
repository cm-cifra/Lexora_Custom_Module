from odoo import fields, models, api


class SaleCustomRecord(models.Model):
    _name = "sale.custom.record"
    _description = "Sale Custom Record"

    sale_order_id = fields.Many2one("sale.order", string="Sales Order", required=True)
    purchase_order = fields.Char(related="sale_order_id.client_order_ref", store=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    product_sku = fields.Char(related="product_id.default_code", store=True)
    carrier = fields.Many2one(
        comodel_name="delivery.carrier",
        string="Carrier",
        related="sale_order_id.x_studio_carrier",
        store=True,
    )
    return_date = fields.Date(string="Return Date")
    status = fields.Selection(
        [
              ("good", "Good"),
            ("damaged", "Damaged"),
        ],
        default="good",
        string="Status",
    )
    notes = fields.Text(string="Notes")
    ship_date = fields.Date(string="Ship Date")

    # 👇 Custom save button logic
    def action_save(self):
        """Custom save action: right now it just writes current values."""
        for rec in self:
            rec.write({})  # This forces saving
        return True
