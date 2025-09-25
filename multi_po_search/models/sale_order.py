import re
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order = fields.Char(string="Purchase Order")

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline into tokens."""
        if not text:
            return []
        return [t for t in re.split(r"[,\s;]+", text.strip()) if t]

    def _make_or_domain(self, field, tokens):
        """Return a flat OR domain like ['|','|',cond1,cond2,cond3] with '=' operator."""
        conds = [(field, "=", t) for t in tokens]
        if len(conds) > 1:
            return ["|"] * (len(conds) - 1) + conds
        return conds

    def _search_purchase_order(self, operator, value):
        """
        Custom search ONLY for purchase_order field.
        This won't affect other search domains.
        """
        tokens = self._tokenize(value)
        if not tokens:
            return []

        if len(tokens) > 1:
            return self._make_or_domain("purchase_order", tokens)
        else:
            return [("purchase_order", "=", tokens[0])]
