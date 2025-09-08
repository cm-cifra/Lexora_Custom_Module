from odoo import models, fields, api

class SaleReturnWizard(models.TransientModel):
    _name = "sale.return.wizard"
    _description = "Return Order Wizard"

    return_date = fields.Date(string="Return Date")
    condition = fields.Selection(
        [('new', 'New'), ('used', 'Used'), ('damaged', 'Damaged')],
        string="Condition"
    )
    product_sku = fields.Char(string="Product SKU")

    # store which sale orders were selected
    order_ids = fields.Many2many('sale.order', string="Orders")

    def action_apply(self):
        """Apply changes to selected sale orders"""
        for order in self.order_ids:
            order.write({
                'x_return_date': self.return_date,
                'x_condition': self.condition,
                'product_sku': self.product_sku,
            })
        return {'type': 'ir.actions.act_window_close'}
