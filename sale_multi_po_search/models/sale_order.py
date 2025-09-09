import re
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order = fields.Char(string='Purchase Order')

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon, newline."""
        if not text:
            return []
        return [t for t in re.split(r'[,\s;]+', text.strip()) if t]

    @classmethod
    def _search(cls, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        Intercept search queries on purchase_order field and split multi-token strings.
        """
        new_args = []
        for arg in args:
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                field, operator, value = arg
                if field == "purchase_order" and operator in ("ilike", "=", "like") and value:
                    tokens = cls._tokenize(cls, value)
                    if len(tokens) > 1:
                        conds = [(field, operator, t) for t in tokens]
                        arg = ['|'] * (len(conds) - 1) + conds
            new_args.append(arg)

        return super(SaleOrder, cls)._search(new_args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
