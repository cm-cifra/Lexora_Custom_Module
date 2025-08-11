from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AmazonOrderMapping(models.Model):
    _name = "amazon.order.mapping"
    _description = "Map Amazon order -> Odoo sale.order"

    amazon_order_id = fields.Char(required=True, index=True)
    sale_order_id = fields.Many2one('sale.order', string="Odoo Sale Order", required=True, ondelete='cascade')
    account_id = fields.Many2one('amazon.account', string='Amazon Account', required=True, ondelete='cascade')
    marketplace = fields.Char()
    last_sync = fields.Datetime()

    _sql_constraints = [
        ('order_account_unique', 'unique(amazon_order_id, account_id, marketplace)', 'Order mapping must be unique per account+marketplace'),
    ]
