from odoo import fields, models


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
        default="pending",
        string="Status",
    )
    notes = fields.Text(string="Notes")
    ship_date = fields.Date(string="Ship Date")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def name_get(self):
        """Display SO number with Purchase Order reference."""
        result = []
        for order in self:
            name = order.name
            if order.client_order_ref:
                name = f"{order.name} - {order.client_order_ref}"
            result.append((order.id, name))
        return result
