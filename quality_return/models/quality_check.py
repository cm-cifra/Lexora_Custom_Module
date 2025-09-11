# -*- coding: utf-8 -*-
from odoo import models, fields

class QualityCheck(models.Model):
    _inherit = "quality.check"

    # Optional helper field if you want to quickly filter in views
    is_return_location = fields.Boolean(
        string="Is Return",
        compute="_compute_is_return",
        store=False
    )

    def _compute_is_return(self):
        for rec in self:
            rec.is_return_location = (
                rec.x_location and rec.x_location.startswith("WH/IN/RETURN")
            )
