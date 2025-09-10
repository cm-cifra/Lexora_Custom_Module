import re
from odoo import models, fields


class ReturnsReport(models.Model):
    _inherit = "returns.report"   # inherit your existing model

    # Add purchase_order field from related stock.picking
    purchase_order = fields.Char(
        string="Purchase Order",
        related="move_line_id.picking_id.purchase_id.name",
        store=True,
    )

    # --- Multi-search on purchase_order ---
    def _tokenize(self, text):
        """Split input by whitespace, comma, semicolon into tokens."""
        if not text:
            return []
        tokens = re.split(r"[,\s;]+", text.strip())
        return [t for t in tokens if t]

    def _build_token_domain(self, search_input):
        """Return OR-chained domain for tokens on purchase_order field."""
        tokens = self._tokenize(search_input)
        if not tokens:
            return []
        conds = [("purchase_order", "ilike", t) for t in tokens]
        return conds if len(conds) == 1 else ["|"] * (len(conds) - 1) + conds

    def name_search(self, name, args=None, operator="ilike", limit=100):
        """Allow searching multiple POs separated by comma/space/semicolon"""
        args = args or []
        if name:
            token_domain = self._build_token_domain(name)
            recs = self.search(token_domain + args, limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)
