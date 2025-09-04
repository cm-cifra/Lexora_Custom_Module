from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Boolean field to identify return orders
    is_return_order = fields.Boolean(
        string="Is Return Order",
        compute="_compute_is_return_order",
        store=True
    )

    @api.depends()  # <-- remove 'order_state' to avoid dependency error
    def _compute_is_return_order(self):
        for order in self:
            # Use getattr in case the field is not loaded yet
            order_state = getattr(order, 'order_state', False)
            order.is_return_order = order_state in ['return_initiated', 'returned']

    # Method to get all return orders
    @api.model
    def get_return_orders(self):
        return self.search([('order_state', 'in', ['return_initiated', 'returned'])])
