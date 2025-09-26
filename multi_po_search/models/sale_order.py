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

    def _name_search(
        self,
        name,
        args=None,
        operator="ilike",
        limit=100,
        name_get_uid=None,
    ):
        """
        Only apply token split search to `purchase_order` field.
        All other searches behave as usual.
        """
        args = list(args or [])

        if name:
            tokens = self._tokenize(name)
            if tokens:
                # Build OR domain on purchase_order field only
                or_domain = self._make_or_domain("purchase_order", tokens)
                args = ["|"] * (len(or_domain) - 1) + or_domain + args

        _logger.debug("SaleOrder._name_search: name=%s args=%s", name, args)

        return super()._name_search(
            name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
