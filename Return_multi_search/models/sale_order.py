# models/stock_picking.py
import re
from odoo import models, fields

class StockPickingPO(models.Model):
    _inherit = 'stock.picking'
 

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline and return non-empty tokens."""
        if not text:
            return []
        tokens = re.split(r'[,\s;]+', text.strip())
        return [t for t in (tok.strip() for tok in tokens) if t]

    def _build_token_domain(self, search_input):
        """Return OR-chained domain for tokens on purchase_order field."""
        tokens = self._tokenize(search_input)
        if not tokens:
            return []
        conds = [('purchase_order', 'ilike', t) for t in tokens]
        if len(conds) == 1:
            return conds
        return ['|'] * (len(conds) - 1) + conds

    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Use tokenized OR search on purchase_order when user types/pastes text."""
        args = args or []
        if name:
            token_domain = self._build_token_domain(name)
            domain = token_domain + args
            recs = self.search(domain, limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)

