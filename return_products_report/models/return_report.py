 
from odoo import models, fields, api


class SaleCustomRecord(models.Model):
    _name = "sale.custom.record"
    _description = "Sale Custom Addon Record"
    _order = "id desc"

    name = fields.Char(string="Reference", readonly=True)

    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale Order",
        ondelete="set null",
    )

    # PO number is read from sale.order field 'purchase_order' (common custom field name)
    po_number = fields.Char(string="PO Number", related="sale_order_id.purchase_order", store=True)

    # Carrier read from sale.order field 'x_studio_carrier' (custom Studio field)
    carrier = fields.Many2one(
    comodel_name="delivery.carrier",
    string="Carrier",
    related="sale_order_id.x_studio_carrier",
    store=True,
)

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        ondelete="set null",
    )

    # Product SKU / internal reference usually in product.default_code
    product_sku = fields.Char(string="Product SKU", related="product_id.default_code", store=True)

    ship_date = fields.Date(string="Ship Date")
    return_date = fields.Date(string="Return Date")

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("shipped", "Shipped"),
            ("returned", "Returned"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
    )

    notes = fields.Text(string="Notes")

    created_by = fields.Many2one(comodel_name="res.users", string="Created by", default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        # create a readable name
        seq = self.env['ir.sequence'].sudo().next_by_code('sale.custom.record') if self.env['ir.sequence'].search([('code','=', 'sale.custom.record')]) else False
        if seq:
            vals['name'] = seq
        else:
            # fallback
            vals['name'] = vals.get('po_number') or vals.get('name') or 'SCR/%s' % (fields.Date.today())
        rec = super(SaleCustomRecord, self).create(vals)
        return rec

    def action_set_shipped(self):
        for r in self:
            r.status = 'shipped'
            if not r.ship_date:
                r.ship_date = fields.Date.context_today(self)

    def action_set_returned(self):
        for r in self:
            r.status = 'returned'
            if not r.return_date:
                r.return_date = fields.Date.context_today(self) 