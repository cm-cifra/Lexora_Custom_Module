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
    carrier_tracking_ref = fields.Char(
        string="Carrier Tracking Ref",
        compute="_compute_delivery_info",
        store=False
    )

    def _compute_delivery_info(self):
        for order in self:
            pickings = order.picking_ids.filtered(lambda p: p.state in ['assigned', 'done', 'confirmed'])
            if pickings:
                last_picking = pickings[-1]
                order.delivery_date = last_picking.date_done
                order.expected_delivery_date = last_picking.scheduled_date
                order.carrier_name = last_picking.carrier_id.name
                order.carrier_tracking_ref = last_picking.carrier_tracking_ref
            else:
                order.delivery_date = False
                order.expected_delivery_date = False
                order.carrier_name = False
                order.carrier_tracking_ref = False
