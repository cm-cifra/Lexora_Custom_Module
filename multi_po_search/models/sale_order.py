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

    def _make_or_domain(self, field, tokens, operator="="):
        """Return a flat OR domain like ['|','|',cond1,cond2,cond3]."""
        conds = [(field, operator, t) for t in tokens]
        if len(conds) > 1:
            return ["|"] * (len(conds) - 1) + conds
        return conds

    def _search_purchase_order(self, operator, value):
        """
        Custom search ONLY for purchase_order field.
        Supports multiple tokens separated by space/comma/semicolon.
        Other fields are not affected.
        """
        tokens = self._tokenize(value)
        if not tokens:
            return []

        # Example: searching "PO123 PO456" will match any of them (OR).
        return self._make_or_domain("purchase_order", tokens, operator)
