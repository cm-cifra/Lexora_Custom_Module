from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_date = fields.Datetime(
        string="Delivery Date",
        compute="_compute_delivery_info",
        store=False
    )
    expected_delivery_date = fields.Datetime(
        string="Expected Delivery Date",
        compute="_compute_delivery_info",
        store=False
    )
    carrier_name = fields.Char(
        string="Carrier",
        compute="_compute_delivery_info",
        store=False
    )

    def _compute_delivery_info(self):
        for order in self:
            pickings = order.picking_ids.filtered(lambda p: p.state == 'done')
            if pickings:
                order.delivery_date = pickings[-1].date_done
                order.carrier_name = pickings[-1].carrier_id.name
                order.expected_delivery_date = pickings[-1].scheduled_date
            else:
                order.delivery_date = False
                order.expected_delivery_date = False
                order.carrier_name = False
