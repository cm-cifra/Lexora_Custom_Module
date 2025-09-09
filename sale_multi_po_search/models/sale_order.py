import re
from odoo import models, fields

class SaleOrderPO(models.Model):
    _inherit = 'sale.order'

    purchase_order = fields.Char(string='Purchase Order')

    def _build_token_domain(self, search_input):
        """Split input into tokens (space, comma, semicolon, newline) 
        and build OR domain on purchase_order field"""
        # Split by whitespace, comma, semicolon, newline
        tokens = re.split(r'[\s,;]+', search_input.strip())
        tokens = [t for t in tokens if t]  # remove empty tokens

        domain = []
        for token in tokens:
            domain.append(('purchase_order', 'ilike', token))

        if not domain:
            return []
        elif len(domain) == 1:
            return domain
        else:
            # Build OR chain: ['|','|', cond1, cond2, cond3...]
            combined_domain = domain[0]
            for token_domain in domain[1:]:
                combined_domain = ['|', combined_domain, token_domain]
            return combined_domain

    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            token_domain = self._build_token_domain(name)
            args = token_domain + args
        return super().name_search(name, args=args, operator=operator, limit=limit)
