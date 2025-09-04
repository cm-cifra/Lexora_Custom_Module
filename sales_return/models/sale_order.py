from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Boolean field to identify return orders
    is_return_order = fields.Boolean(
        string="Is Return Order",
        compute="_compute_is_return_order",
        store=True
    )

    @api.depends('order_state')  # <-- FIXED: use order_state not state
    def _compute_is_return_order(self):
        for order in self:
            order.is_return_order = order.order_state in ['return_initiated', 'returned']

    # Optional: method to get only return orders
    @api.model
    def get_return_orders(self):
        return self.search([('order_state', 'in', ['return_initiated', 'returned'])])
