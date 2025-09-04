from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Declare the existing selection field
    order_state = fields.Selection(
        selection=[
            ('po', 'PO'),
            ('backorder', 'Backorders'),
            ('process', 'Processed'),
            ('ship', 'Shipped'),
            ('cancel', 'Cancelled'),
            ('return_initiated', 'Return Initiated'),
            ('returned', 'Returned'),
        ],
        string='Order State',
        store=True
    )

    # Boolean field to identify return orders
    is_return_order = fields.Boolean(
        string="Is Return Order",
        compute="_compute_is_return_order",
        store=True
    )

    @api.depends('order_state')
    def _compute_is_return_order(self):
        for order in self:
            order.is_return_order = order.order_state in ['return_initiated', 'returned']

    @api.model
    def get_return_orders(self):
        return self.search([('order_state', 'in', ['return_initiated', 'returned'])])
