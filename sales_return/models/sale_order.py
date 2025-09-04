from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Quotation Sent'),
            ('sale', 'Sales Order'),
            ('return_initiated', 'Return Initiated'),
            ('returned', 'Returned'),
        ],
        string="Order State",
        default='draft'
    )

    is_return_order = fields.Boolean(
        string="Is Return Order",
        compute="_compute_is_return_order",
        store=True
    )

    # 🔹 New custom fields
    x_return_date = fields.Date(string="Return Date")
    x_condition = fields.Selection(
        selection=[
            ('new', 'New'),
            ('used', 'Used'),
            ('damaged', 'Damaged'),
        ],
        string="Condition"
    )
    product_sku = fields.Char(string="Product SKU")

    @api.depends('order_state')
    def _compute_is_return_order(self):
        for order in self:
            order.is_return_order = order.order_state in ['return_initiated', 'returned']
