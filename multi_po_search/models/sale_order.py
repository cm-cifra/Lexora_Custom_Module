import re
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order = fields.Char(string="Purchase Order")

    def _tokenize(self, text):
        """Split by whitespace, comma, semicolon or newline into tokens."""
        if not text:
            return []
        return [t for t in re.split(r"[,\s;]+", text.strip()) if t]

    @api.model
    def _search_purchase_order(self, operator, value):
        """
        Custom search ONLY for purchase_order field.

        - Supports multiple tokens separated by space/comma/semicolon.
        - Returns a domain on 'id' (not on 'purchase_order'), avoiding recursion.
        """
        tokens = self._tokenize(value)
        if not tokens:
            # no tokens → produce a domain that matches nothing
            return [('id', 'in', [])]

        # Normalize operator and decide SQL operator / parameter formatting
        op = (operator or '').lower()
        params = []
        clauses = []

        if op in ('ilike', 'like'):
            sql_op = 'ILIKE' if op == 'ilike' else 'LIKE'
            for t in tokens:
                clauses.append(f"purchase_order {sql_op} %s")
                params.append(f"%{t}%")
        elif op in ('=', '=='):
            for t in tokens:
                clauses.append("purchase_order = %s")
                params.append(t)
        else:
            # fallback: use ILIKE behaviour (friendly for user searches)
            for t in tokens:
                clauses.append("purchase_order ILIKE %s")
                params.append(f"%{t}%")

        # Build and run a safe parametrized SQL query against the sale_order table.
        # Using self._table prevents hard-coding the table name.
        where_sql = " OR ".join(clauses)
        if not where_sql:
            return [('id', 'in', [])]

        sql = f"SELECT id FROM {self._table} WHERE {where_sql}"
        self.env.cr.execute(sql, params)
        rows = self.env.cr.fetchall()
        ids = [r[0] for r in rows]

        # Return a domain on id — this will not trigger `_search_purchase_order` again.
        return [('id', 'in', ids)]
