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
        - Supports multiple tokens separated by space/comma/semicolon.
        - Builds an OR domain so any token can match.
        - Does not affect other search fields.
        """
        tokens = self._tokenize(value)
        if not tokens:
            return [('id', '=', 0)]  # match nothing

        conds = [("purchase_order", operator, t) for t in tokens]

        if len(conds) > 1:
            # Build flat OR domain: ["|", cond1, cond2, cond3, ...]
            return ["|"] * (len(conds) - 1) + conds
        return conds
