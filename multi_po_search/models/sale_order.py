import re
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order = fields.Char(
        string="Purchase Order",
        search="_search_purchase_order",  # custom search
    )

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon, or newline into tokens."""
        if not text:
            return []
        return [t for t in re.split(r"[,\s;]+", text.strip()) if t]

    @api.model
    def _search_purchase_order(self, operator, value):
        """
        Custom search ONLY for purchase_order field.
        - Tokens separated by space/comma/semicolon.
        - Uses '=' operator to avoid LIKE spillover into other searches.
        - Builds an AND domain (all tokens must match).
        """
        tokens = self._tokenize(value)
        if not tokens:
            return [("id", "=", 0)]  # match nothing

        # Force '=' operator for clean PO search
        conds = [("purchase_order", "=", t) for t in tokens]

        if len(conds) > 1:
            # Build AND domain: all tokens must match
            domain = conds[0]
            for cond in conds[1:]:
                domain = ["&", domain, cond]
            return domain
        return conds
