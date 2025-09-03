from odoo import fields, models, api


class SaleCustomRecord(models.Model):
    _name = "sale.custom.record"
    _description = "Sale Return Report"
    _rec_name = "sale_order_id"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sales Order", required=True, ondelete="cascade"
    )

    order_line_id = fields.Many2one(
        "sale.order.line",
        string="Order Line",
        required=True,
        domain="[('order_id', '=', sale_order_id)]",
    )

    # Snapshot fields
    purchase_order = fields.Char(string="Customer PO")
    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    product_sku = fields.Char(string="Product SKU", readonly=True)

    # ✅ FIX: carrier must be Many2one, not Char
    carrier = fields.Many2one("delivery.carrier", string="Carrier")

    return_date = fields.Date(string="Return Date")
    ship_date = fields.Date(string="Ship Date")

    status = fields.Selection(
        [
            ("good", "Good"),
            ("damaged", "Damaged"),
        ],
        default="good",
        string="Status",
    )
    notes = fields.Text(string="Notes")

    @api.onchange("sale_order_id")
    def _onchange_sale_order_id(self):
        """Auto-fill purchase order + carrier when Sales Order is chosen."""
        for rec in self:
            if rec.sale_order_id:
                rec.purchase_order = rec.sale_order_id.client_order_ref
                rec.carrier = (
                    rec.sale_order_id.x_studio_carrier.id
                    if rec.sale_order_id.x_studio_carrier
                    else False
                )
                rec.order_line_id = False  # reset line if SO changes

    @api.onchange("order_line_id")
    def _onchange_order_line_id(self):
        """Auto-fill product + SKU when order line is chosen."""
        for rec in self:
            if rec.order_line_id:
                rec.product_id = rec.order_line_id.product_id
                rec.product_sku = rec.order_line_id.product_id.default_code

    def action_save(self):
        """Custom save button (record stays in return report)."""
        return True
