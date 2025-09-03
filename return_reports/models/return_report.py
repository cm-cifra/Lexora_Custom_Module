from odoo import models, fields, api

class ReturnReport(models.Model):
    _name = 'return.report'
    _description = 'Return Report'

    date = fields.Date(string="Return Date", default=fields.Date.context_today)

    merchant_id = fields.Many2one(
        'res.partner',
        string="Merchant",
    )

    po_id = fields.Many2one('sale.order', string="Sales Order")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier")

    condition = fields.Selection([
        ('good', 'Good'),
        ('damaged', 'Damaged')
    ], string="Condition", default='good')

    return_date = fields.Date(string="Return Date", default=fields.Date.context_today)

    shipped_date = fields.Datetime(
        string="Shipped Date",
        compute="_compute_shipped_date",
        store=True,
        readonly=False,
    )

    note = fields.Text(string="Notes")
    line_ids = fields.One2many('return.report.line', 'report_id', string="Return Lines")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string="Status", default='draft', tracking=True)

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
