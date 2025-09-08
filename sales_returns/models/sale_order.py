from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    latest_quality_state = fields.Selection(
        [
            ("no", "No Checks"),
            ("fail", "Failed"),
            ("pass", "Passed"),
            ("progress", "In Progress"),
        ],
        string="Latest Quality Check",
        compute="_compute_latest_quality_state",
        store=False,  # set to True if you want to persist
    )

    @api.depends("picking_ids")
    def _compute_latest_quality_state(self):
        QualityCheck = self.env["quality.check"]
        for order in self:
            checks = QualityCheck.search(
                [("picking_id", "in", order.picking_ids.ids)],
                order="id desc",
                limit=1,
            )
            if not checks:
                order.latest_quality_state = "no"
            else:
                order.latest_quality_state = checks.quality_state or "progress"
