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

    def _make_or_domain(self, field, operator, tokens):
        """Build a properly nested OR domain from tokens."""
        if not tokens:
            return []
        domain = (field, operator, tokens[0])
        for token in tokens[1:]:
            domain = ["|", domain, (field, operator, token)]
        return domain

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        """Intercept purchase_order ilike/like/= searches and expand into OR tokens."""
        expanded_domain = []
        for arg in domain:
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                field, operator, value = arg
                if field == "purchase_order" and operator in ("ilike", "like", "=") and value:
                    tokens = self._tokenize(value)
                    if len(tokens) > 1:
                        expanded_domain.append(self._make_or_domain(field, operator, tokens))
                        continue  # skip adding arg itself
            expanded_domain.append(arg)

        # Now flatten in case nested domains exist
        final_domain = []
        for d in expanded_domain:
            if isinstance(d, list) and d and d[0] == "|":
                # Already a valid domain, extend it
                final_domain.extend(d if isinstance(d, list) else [d])
            else:
                final_domain.append(d)

        return super()._search(
            final_domain,
            offset=offset,
            limit=limit,
            order=order,
            access_rights_uid=access_rights_uid,
        )
