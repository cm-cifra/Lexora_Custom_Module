# -*- coding: utf-8 -*-
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    is_return_reference = fields.Boolean(
        string="Is Return (Reference)",
        compute="_compute_is_return_reference",
        store=False,
    )

    def _compute_is_return_reference(self):
        """Mark move lines as return if reference starts with WH/IN/RETURN"""
        for rec in self:
            rec.is_return_reference = bool(
                rec.reference and rec.reference.startswith("WH/IN/RETURN")
            )
