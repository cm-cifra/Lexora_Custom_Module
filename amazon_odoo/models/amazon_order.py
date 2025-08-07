from odoo import models, fields

class AmazonOrder(models.Model):
    _name = 'amazon.order'
    _description = 'Amazon Order'

    order_id = fields.Char(string='Order ID', required=True)
    buyer_name = fields.Char(string='Buyer Name')
    purchase_date = fields.Datetime(string='Purchase Date')
    order_total = fields.Float(string='Order Total')
    order_status = fields.Selection([
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ], string='Order Status', default='pending')
