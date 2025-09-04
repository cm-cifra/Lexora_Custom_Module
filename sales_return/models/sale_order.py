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

    @api.depends('order_state')  # <-- depends on your new field
    def _compute_is_return_order(self):
        for order in self:
            order.is_return_order = order.order_state in ['return_initiated', 'returned']
