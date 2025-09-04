from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class ReturnReport(models.Model):
    _name = 'return.report'
    _description = 'Return Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string="Return Date", default=fields.Date.context_today)
    merchant_id = fields.Many2one('res.partner', string="Merchant")

    po_id = fields.Many2one('sale.order', string="Sales Order")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier")
    return_id = fields.Char(string=' ', readonly=True)  # auto-generated after confirm
    x_po = fields.Char(string='PO #') 
    prod_sku = fields.Char(string='Sku')
    condition = fields.Selection([
        ('good', 'Good'),
        ('damaged', 'Damaged')
    ], string="Condition", default='good')

    return_date = fields.Date(string="Return Date", default=fields.Date.context_today)

    shipped_date = fields.Datetime(
        string="Shipped Date",
        compute="_compute_shipped_date",
        store=True,
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
            if rec.state != 'draft':
                raise UserError("You can only confirm a draft return report.")

            # Generate RETURN number if not already generated
            if not rec.return_id:
                date_str = fields.Date.today().strftime('%Y/%m')
                seq_number = self.env['ir.sequence'].next_by_code('return.report') or '001'
                
                # Append x_po at the end if available
                po_str = f"/{rec.x_po}" if rec.x_po else ""
                rec.return_id = f'RETURN/{date_str}/{seq_number.zfill(4)}{po_str}'

            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError("You can only mark confirmed reports as done.")
            rec.state = 'done'


class ReturnReportLine(models.Model):
    _name = 'return.report.line'
    _description = 'Return Report Line'

    report_id = fields.Many2one('return.report', string="Return Report", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    reason = fields.Text(string="Reason")
