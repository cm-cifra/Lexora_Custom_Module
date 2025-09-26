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

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        """
        Add extra purchase_order search handling without modifying other search behavior.
        """
        new_domain = list(domain)  # keep original intact

        # Collect additional conditions separately
        extra_domain = []
        for arg in domain:
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                field, operator, value = arg
                if field == "purchase_order" and operator in ("ilike", "like", "=") and value:
                    tokens = self._tokenize(value)
                    if len(tokens) > 1:
                        extra_domain.extend(self._make_or_domain(field, tokens))
                    else:
                        extra_domain.append((field, "=", tokens[0]))

        # If extra domain was built, combine with original domain using OR
        if extra_domain:
            if len(extra_domain) > 1:
                new_domain = ["|"] * (len(extra_domain) - 1) + extra_domain + new_domain
            else:
                new_domain = ["|", extra_domain[0], new_domain]

        return super()._search(
            new_domain,
            offset=offset,
            limit=limit,
            order=order,
            access_rights_uid=access_rights_uid,
        )
