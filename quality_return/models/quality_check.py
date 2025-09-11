# -*- coding: utf-8 -*-
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    is_return_location = fields.Boolean(
        string="Is Return",
        compute="_compute_is_return",
        store=False,
    )

    def _compute_is_return(self):
        """Mark move lines whose destination location is a return location."""
        for rec in self:
            rec.is_return_location = bool(
                rec.location_dest_id and rec.location_dest_id.display_name.startswith("WH/IN/RETURN")
            )
