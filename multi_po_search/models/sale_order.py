import re
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order = fields.Char(string="Purchase Order")

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline into tokens."""
        if not text:
            return []
        return [t for t in re.split(r"[,\s;]+", text.strip()) if t]

    @api.model
    def _search_purchase_order(self, operator, value):
        """
        Custom search ONLY for purchase_order field.
        Supports multiple tokens separated by space/comma/semicolon.
        Example: "123 324 132 054" → matches any of those.
        """
        tokens = self._tokenize(value)
        if not tokens:
            return [('id', 'in', [])]

        # Only support '=' and 'ilike' style operators
        op = (operator or '').lower()
        if op in ('=', '=='):
            # Exact match on any of the tokens
            return [('purchase_order', 'in', tokens)]
        else:
            # For like/ilike → OR conditions
            or_domain = []
            for t in tokens:
                or_domain.append(('purchase_order', operator, t))
            if len(or_domain) > 1:
                # build flat OR: ['|','|', cond1, cond2, cond3]
                return ['|'] * (len(or_domain) - 1) + or_domain
            return or_domain
