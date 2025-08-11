from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AmazonAccount(models.Model):
    _name = "amazon.account"
    _description = "Amazon Account config"

    name = fields.Char(required=True)  # label
    account_name = fields.Char(required=True, help="Account name used to sync")
    home_marketplace = fields.Char(required=True, help="Marketplace code, e.g. US, UK")
    client_id = fields.Char(string="Client ID")
    client_secret = fields.Char(string="Client Secret")
    refresh_token = fields.Char(string="Refresh Token / credentials")
    api_type = fields.Selection([('sp','SP-API'), ('mws','MWS')], default='sp')
    active = fields.Boolean(default=True)

    def get_client(self):
        """
        Return an AmazonAPIClient instance configured for this account.
        Implementation left abstract — inject SP-API/MWS implementation here.
        """
        self.ensure_one()
        from ..services.amazon_client import AmazonAPIClient
        return AmazonAPIClient(self)
    def _cron_sync_products(self):
        """Iterate active accounts and sync products"""
        for acc in self.search([('active','=',True)]):
            client = acc.get_client()
            items = client.fetch_products()
            for item in items:
                self.env['amazon.product.mapping'].create_or_update_from_amazon(acc, item)

    def _cron_sync_orders(self):
        """Iterate accounts and sync orders"""
        for acc in self.search([('active','=',True)]):
            client = acc.get_client()
            orders = client.fetch_orders()
            for od in orders:
                self._create_or_update_order_from_amazon(acc, od)

    def _create_or_update_order_from_amazon(self, account, order_data):
        """
        Create sale.order if mapping not present. Use account_name + home_marketplace for uniqueness.
        """
        OrderMap = self.env['amazon.order.mapping']
        existing = OrderMap.search([('amazon_order_id','=',order_data.get('order_id')), ('account_id','=',account.id), ('marketplace','=',account.home_marketplace)], limit=1)
        if existing:
            _logger.info("Order %s already imported", order_data.get('order_id'))
            return existing.sale_order_id
        # create partner
        partner_vals = {
            'name': order_data.get('buyer', {}).get('name') or 'Amazon Buyer',
            'email': order_data.get('buyer', {}).get('email'),
            'street': order_data.get('shipping', {}).get('address1'),
            'city': order_data.get('shipping', {}).get('city'),
            'zip': order_data.get('shipping', {}).get('postal_code'),
            'country_id': False,
        }
        partner = self.env['res.partner'].create(partner_vals)
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'client_order_ref': order_data.get('order_id'),
        })
        # add order lines
        for line in order_data.get('items', []):
            sku = line.get('sku')
            mapping = self.env['amazon.product.mapping'].search([('amazon_sku','=',sku), ('account_id','=',account.id)], limit=1)
            product = mapping.product_id if mapping else self.env['product.product'].search([('default_code','=',sku)], limit=1)
            if not product:
                # fallback: create placeholder product
                tmpl = self.env['product.template'].create({'name': line.get('title') or sku})
                product = self.env['product.product'].create({'product_tmpl_id': tmpl.id, 'default_code': sku})
                # optionally create mapping
                self.env['amazon.product.mapping'].create({
                    'amazon_sku': sku,
                    'asin': line.get('asin'),
                    'product_id': product.id,
                    'account_id': account.id,
                    'marketplace': account.home_marketplace
                })
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': product.display_name,
                'product_uom_qty': line.get('qty') or 1,
                'price_unit': line.get('price') or 0.0,
            })
        OrderMap.create({
            'amazon_order_id': order_data.get('order_id'),
            'sale_order_id': sale_order.id,
            'account_id': account.id,
            'marketplace': account.home_marketplace,
        })
        return sale_order
