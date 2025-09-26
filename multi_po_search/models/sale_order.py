import re
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order = fields.Char(string="Purchase Order")

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline into tokens."""
        if not text:
            return []
        return [t for t in re.split(r"[,\s;]+", text.strip()) if t]

    def _make_or_domain(self, field, tokens):
        """Return a flat OR domain like ['|','|', cond1, cond2, cond3] with '=' operator."""
        conds = [(field, "=", t) for t in tokens]
        if len(conds) > 1:
            return ["|"] * (len(conds) - 1) + conds
        return conds

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        """
        Expand purchase_order searches (tokenize and turn into '=' matches)
        without breaking other domain clauses.
        Example: ('purchase_order','ilike','PO1 PO2') -> ['|',('purchase_order','=','PO1'),('purchase_order','=','PO2')]
        inserted *in place* of the original purchase_order clause.
        """
        if not domain:
            return super()._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)

        new_domain = []
        modified = False

        for clause in domain:
            # only transform simple 3-item clauses; keep operators and nested lists untouched
            if isinstance(clause, (list, tuple)) and len(clause) == 3:
                field, operator, value = clause
                if field == "purchase_order" and operator in ("ilike", "like", "=") and value:
                    # strip wildcards if user used ilike/like with %
                    if operator in ("ilike", "like"):
                        value = value.replace("%", "")
                    tokens = self._tokenize(value)
                    if not tokens:
                        # nothing usable — skip the clause (or keep original if you prefer)
                        continue
                    if len(tokens) == 1:
                        # single token → equality match
                        new_domain.append((field, "=", tokens[0]))
                    else:
                        # multiple tokens -> build a flat OR chain
                        # Example tokens = [a,b,c] -> ['|','|', (f,'=',a),(f,'=',b),(f,'=',c)]
                        new_domain.extend(["|"] * (len(tokens) - 1))
                        new_domain.extend((field, "=", t) for t in tokens)
                    modified = True
                    # skip appending original purchase_order clause
                    continue

            # default: keep clause unchanged
            new_domain.append(clause)

        _logger.debug("SaleOrder._search: original_domain=%s --> transformed_domain=%s", domain, (new_domain if modified else domain))

        # if we didn't modify anything, pass the original domain through
        final_domain = new_domain if modified else domain
        return super()._search(final_domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
