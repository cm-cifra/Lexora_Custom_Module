from odoo import fields, models, api


class SaleCustomRecord(models.Model):
    _name = "sale.custom.record"
    _description = "Sale Return Report"
    _rec_name = "sale_order_id"

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sales Order",
        required=True,
        ondelete="cascade",
        domain="[('state', 'in', ['sale', 'done'])]",
    )

    purchase_order = fields.Char(
        string="Customer PO",
        related="sale_order_id.client_order_ref",
        store=True,
        readonly=True,
    )

    carrier_id = fields.Many2one(
        "delivery.carrier",
        string="Carrier",
        help="Carrier for this return report",
    )

    return_date = fields.Date(string="Return Date")
    ship_date = fields.Date(string="Ship Date")

    status = fields.Selection(
        [
            ("good", "Good"),
            ("damaged", "Damaged"),
        ],
        default="good",
        string="Status",
    )
    notes = fields.Text(string="Notes")

    line_ids = fields.One2many(
        "return.report.line",
        "report_id",
        string="Returned Products",
    )

    def action_save(self):
        """Custom save button (record stays in return report)."""
        return True


class ReturnReportLine(models.Model):
    _name = "return.report.line"
    _description = "Return Report Line"

    report_id = fields.Many2one(
        "sale.custom.record",
        string="Return Report",
        required=True,
        ondelete="cascade",
    )

    product_id = fields.Many2one(
        "product.product",
        string="Returned Product",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity to Return",
        default=1.0,
    )

    reason = fields.Char(
        string="Reason for Return",
    )
