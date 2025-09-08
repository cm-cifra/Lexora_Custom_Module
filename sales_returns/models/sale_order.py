from odoo import api, fields, models

class SaleOrderQuality(models.Model):
    _name = "sale.order.quality"
    _description = "Sale Orders with Quality Check"
    _auto = False  # we don't create a new table, it's a reporting model

    sale_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    date_order = fields.Datetime("Order Date", readonly=True)
    amount_total = fields.Monetary("Total", readonly=True)
    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True)
    quality_state = fields.Selection(
        [
            ("no", "No Checks"),
            ("fail", "Failed"),
            ("pass", "Passed"),
            ("progress", "In Progress"),
        ],
        string="Latest Quality Check",
        readonly=True,
    )

    @property
    def _table_query(self):
        """
        Use SQL to build a reporting view combining sale.order + quality.check
        """
        return """
            SELECT
                so.id as id,
                so.id as sale_id,
                so.partner_id as partner_id,
                so.date_order as date_order,
                so.amount_total as amount_total,
                so.currency_id as currency_id,
                COALESCE(qc.quality_state, 'no') as quality_state
            FROM sale_order so
            LEFT JOIN LATERAL (
                SELECT quality_state
                FROM quality_check qc
                JOIN stock_picking sp ON qc.picking_id = sp.id
                WHERE sp.sale_id = so.id
                ORDER BY qc.id DESC
                LIMIT 1
            ) qc ON TRUE
        """
