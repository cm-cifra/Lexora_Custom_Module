# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CustomQualityCheck(models.Model):
    _name = "custom.quality.check"
    _description = "Custom Quality Check"

    # Link to original quality.check
    quality_check_id = fields.Many2one("quality.check", string="Quality Check", ondelete="cascade")

    # Mirror some fields from quality.check for display
    name = fields.Char(related="quality_check_id.name", store=True)
    product_id = fields.Many2one(related="quality_check_id.product_id", store=True)
    lot_id = fields.Many2one(related="quality_check_id.lot_id", store=True)
    result = fields.Selection(related="quality_check_id.quality_state", store=True)
    check_date = fields.Datetime(related="quality_check_id.create_date", store=True)

    # Example: auto populate from quality.check
    @api.model
    def fetch_quality_checks(self):
        """Fetch all quality.check and create/update records"""
        existing_links = self.search([]).mapped("quality_check_id.id")
        checks = self.env["quality.check"].search([])
        for qc in checks:
            if qc.id not in existing_links:
                self.create({"quality_check_id": qc.id})
