import re
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order = fields.Char(string="Purchase Order")

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline into tokens."""
        if not text:
            return []
        return [t for t in re.split(r"[,\s;]+", text.strip()) if t]

    def _make_or_domain(self, field, tokens):
        """Return a flat OR domain like ['|','|', cond1, cond2, cond3] with '=' operator."""
        conds = [(field, "=", t) for t in tokens]
        if len(conds) > 1:
            return ["|"] * (len(conds) - 1) + conds
        return conds

    def search_multi_po(self, purchase_orders, **kwargs):
        """
        Custom search method: find orders by multiple purchase_order values.
        Example: env['sale.order'].search_multi_po("PO1 PO2")
        """
        tokens = self._tokenize(purchase_orders)
        if not tokens:
            return self.browse()  # return empty recordset

        domain = self._make_or_domain("purchase_order", tokens)
        _logger.debug("SaleOrder.search_multi_po: tokens=%s domain=%s", tokens, domain)

        return self.search(domain, **kwargs)
