# models/sale_order.py
import re
from odoo import models, fields

class SaleOrderPO(models.Model):
    _inherit = 'sale.order'

    # If purchase_order already exists in your DB, you can remove this field definition.
    purchase_order = fields.Char(string='Purchase Order')

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline and return non-empty tokens."""
        if not text:
            return []
        # split on spaces, newlines, commas, semicolons, tabs etc.
        tokens = re.split(r'[,\s;]+', text.strip())
        return [t for t in (tok.strip() for tok in tokens) if t]

    def _build_token_domain(self, search_input):
        """Return OR-chained domain for tokens on purchase_order field.

        Example for 3 tokens -> ['|', '|', cond1, cond2, cond3]
        """
        tokens = self._tokenize(search_input)
        if not tokens:
            return []
        conds = [('purchase_order', 'ilike', t) for t in tokens]
        if len(conds) == 1:
            return conds
        # Prepend (n-1) '|' operators followed by all conditions:
        return ['|'] * (len(conds) - 1) + conds

    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Use tokenized OR-domain search on purchase_order when user types/pastes text."""
        args = args or []
        if name:
            token_domain = self._build_token_domain(name)
            domain = token_domain + args
            # Perform the search using our custom domain and return the (id, display_name) tuples
            recs = self.search(domain, limit=limit)
            return recs.name_get()
        # Fallback to default behaviour when no name provided
        return super().name_search(name, args=args, operator=operator, limit=limit)
