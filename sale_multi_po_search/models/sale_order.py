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

    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """Intercept purchase_order ilike searches and expand into OR tokens."""
        new_domain = []
        for arg in domain:
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                field, operator, value = arg
                if field == "purchase_order" and operator in ("ilike", "like", "=") and value:
                    tokens = self._tokenize(value)
                    if len(tokens) > 1:
                        conds = [(field, operator, t) for t in tokens]
                        arg = ["|"] * (len(conds) - 1) + conds
            new_domain.append(arg)

        return super()._search(
            new_domain,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
