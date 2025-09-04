from odoo import models, fields, api

class ReturnReport(models.Model):
    _name = 'return.report'
    _description = 'Return Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # add chatter

    date = fields.Date(string="Return Date", default=fields.Date.context_today, tracking=True)
    merchant_id = fields.Many2one('res.partner', string="Merchant", tracking=True)

    po_id = fields.Many2one('sale.order', string="Sales Order")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier")
    x_po = fields.Char(string='Po #')
    prod_sku = fields.Char(string='Sku')
    condition = fields.Selection([
        ('good', 'Good'),
        ('damaged', 'Damaged')
    ], string="Condition", default='good', tracking=True)

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

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        compute='_compute_sale_order',
        store=False
    )

    @api.depends('po_id', 'x_po')
    def _compute_shipped_date(self):
        for rec in self:
            rec.shipped_date = rec.po_id.x_studio_date_shipped if rec.po_id else False

    @api.depends('x_po')
    def _compute_sale_order(self):
        SaleOrder = self.env['sale.order']
        for rec in self:
            rec.sale_order_id = SaleOrder.search([('purchase_order', '=', rec.x_po)], limit=1)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    # New method for "Open Sale Order" button
    def action_open_sale_order(self):
        self.ensure_one()
        if self.sale_order_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale Order',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': self.sale_order_id.id,
                'target': 'current',
            }
        return False


class ReturnReportLine(models.Model):
    _name = 'return.report.line'
    _description = 'Return Report Line'

    report_id = fields.Many2one('return.report', string="Return Report", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    reason = fields.Text(string="Reason")
``
