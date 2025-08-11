# services/amazon_client.py
import logging
from odoo import _
_logger = logging.getLogger(__name__)

class AmazonAPIClient:
    def __init__(self, account):
        self.account = account
        # configure client based on account.api_type and credentials
        # For real use: build SP-API OAuth & signer or MWS signature here.

    def fetch_products(self, since=None):
        """
        Return iterable of product dicts. In production this calls Amazon SP-API or MWS.
        Example dict: {'sku':'SKU123', 'asin':'B0XXXX', 'title':'Product', 'price': '12.45'}
        """
        # placeholder - implement real call.
        _logger.info("Fetching products for account %s marketplace %s", self.account.account_name, self.account.home_marketplace)
        return []

    def fetch_orders(self, since=None):
        """
        Return iterable of order dicts. Example:
        {'order_id':'AMZ123', 'buyer': {...}, 'items': [{'sku':'SKU123','qty':1,'price':12.5}], 'total': 12.5}
        """
        _logger.info("Fetching orders for account %s", self.account.account_name)
        return []
