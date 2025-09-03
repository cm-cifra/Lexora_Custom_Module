from odoo import models, fields

class ReturnReport(models.Model):
    _name = 'return.report'
    _description = 'Return Report'

    date = fields.Date(string="Return Date", default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string="Customer", readonly=True)
    merchant_id = fields.Many2one('res.partner', string="Merchant", readonly=True)
    po_id = fields.Many2one('sale.order', string="Sales Order")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier")
    condition = fields.Selection([
        ('good', 'Good'),
        ('damaged', 'Damaged')
    ], string="Condition", default='good')
    return_date = fields.Date(string="Return Date", default=fields.Date.context_today)
    shipped_date = fields.Datetime(string="Shipped Date", related="po_id.date_order", store=True, readonly=True)
    note = fields.Text(string="Notes")
    line_ids = fields.One2many('return.report.line', 'report_id', string="Return Lines")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string="Status", default='draft', tracking=True)

    def action_confirm(self):
        """Move report to Confirmed state"""
        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):
        """Move report to Done state"""
        for rec in self:
            rec.state = 'done'
