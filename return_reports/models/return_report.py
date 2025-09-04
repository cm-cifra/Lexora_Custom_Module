from odoo import models, fields, api


class ReturnReport(models.Model):
    _name = 'return.report'
    _description = 'Return Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # optional: adds chatter

    date = fields.Date(
        string="Report Date",
        default=fields.Date.context_today,
        tracking=True,
    )
    merchant_id = fields.Many2one(
        'res.partner',
        string="Merchant",
        tracking=True,
    )
    po_id = fields.Many2one(
        'sale.order',
        string="Sales Order",
        tracking=True,
    )
    carrier_id = fields.Many2one(
        'delivery.carrier',
        string="Carrier",
    )

    condition = fields.Selection(
        [('good', 'Good'),
         ('damaged', 'Damaged')],
        string="Condition",
        default='good',
    )

    return_date = fields.Date(
        string="Return Date",
        default=fields.Date.context_today,
    )
    shipped_date = fields.Datetime(
        string="Shipped Date",
        compute="_compute_shipped_date",
        store=True,
    )
    note = fields.Text(string="Notes")

    line_ids = fields.One2many(
        'return.report.line',
        'report_id',
        string="Return Lines",
        copy=True,
    )

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('done', 'Done')],
        string="Status",
        default='draft',
        tracking=True,
        copy=False,
    )

    @api.depends('po_id')
    def _compute_shipped_date(self):
        for rec in self:
            rec.shipped_date = rec.po_id.x_studio_date_shipped if rec.po_id else False

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            rec.state = 'done'


class ReturnReportLine(models.Model):
    _name = 'return.report.line'
    _description = 'Return Report Line'

    report_id = fields.Many2one(
        'return.report',
        string="Return Report",
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        required=True,
    )
    sku = fields.Char(
        string="SKU",
        compute="_compute_sku",
        store=True,
        readonly=True,
    )
    quantity = fields.Float(
        string="Quantity",
        default=1.0,
    )
    reason = fields.Selection(
        [('damaged', 'Damaged'),
         ('wrong_item', 'Wrong Item Sent'),
         ('not_needed', 'Not Needed'),
         ('other', 'Other')],
        string="Reason",
    )

    @api.depends('product_id')
    def _compute_sku(self):
        for line in self:
            line.sku = line.product_id.default_code or False
