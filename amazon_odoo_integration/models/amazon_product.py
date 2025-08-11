from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AmazonProductMapping(models.Model):
    _name = "amazon.product.mapping"
    _description = "Map Amazon item -> Odoo product"

    amazon_sku = fields.Char(required=True, index=True)
    asin = fields.Char(index=True)
    product_id = fields.Many2one('product.product', string="Odoo Product", required=True, ondelete='cascade')
    account_id = fields.Many2one('amazon.account', string='Amazon Account', required=True, ondelete='cascade')
    marketplace = fields.Char()
    last_sync = fields.Datetime()

    _sql_constraints = [
        ('sku_account_unique', 'unique(amazon_sku, account_id, marketplace)', 'Mapping must be unique per account+marketplace'),
    ]

    @api.model
    def create_or_update_from_amazon(self, account, item):
        """
        item is a dict from Amazon: {'sku':..., 'asin':..., 'title':..., 'price':..., ...}
        This demo will create product.template + product.product if not present.
        """
        Product = self.env['product.product']
        ProductTemplate = self.env['product.template']
        sku = item.get('sku')
        asin = item.get('asin')

        # find existing mapping
        mapping = self.search([('amazon_sku', '=', sku), ('account_id','=',account.id), ('marketplace','=',account.home_marketplace)], limit=1)
        if mapping:
            product = mapping.product_id
        else:
            # create basic product
            template = ProductTemplate.create({
                'name': item.get('title') or sku,
            })
            product = Product.create({
                'product_tmpl_id': template.id,
                'default_code': sku,
            })
            mapping = self.create({
                'amazon_sku': sku,
                'asin': asin,
                'product_id': product.id,
                'account_id': account.id,
                'marketplace': account.home_marketplace,
            })
        # update product values (price/description etc.)
        # Note: Odoo pricing usually handled on pricelist; for demo we attach list_price
        price = item.get('price')
        if price:
            product.product_tmpl_id.list_price = float(price)
        mapping.last_sync = fields.Datetime.now()
        return mapping
