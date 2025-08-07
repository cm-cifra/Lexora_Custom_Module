from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AmazonProduct(models.Model):
    _name = 'amazon.product'
    _description = 'Amazon Product'

    name = fields.Char(string="Amazon Product Name", required=True)
    amazon_sku = fields.Char(string="Amazon SKU", required=True)
    amazon_barcode = fields.Char(string="Amazon Barcode")
    odoo_product_id = fields.Many2one('product.product', string="Mapped Odoo Product", compute='_compute_odoo_product', store=True)

    match_type = fields.Selection([
        ('barcode', 'Barcode'),
        ('sku', 'Internal Reference'),
        ('none', 'No Match'),
    ], string="Match Type", compute='_compute_match_type', store=True)

    @api.depends('amazon_sku', 'amazon_barcode')
    def _compute_odoo_product(self):
        for record in self:
            product = None
            if record.amazon_barcode:
                product = self.env['product.product'].search([('barcode', '=', record.amazon_barcode)], limit=1)
            if not product and record.amazon_sku:
                product = self.env['product.product'].search([('default_code', '=', record.amazon_sku)], limit=1)
            record.odoo_product_id = product.id if product else False

    @api.depends('amazon_sku', 'amazon_barcode', 'odoo_product_id')
    def _compute_match_type(self):
        for record in self:
            if record.odoo_product_id:
                if record.amazon_barcode and record.amazon_barcode == record.odoo_product_id.barcode:
                    record.match_type = 'barcode'
                elif record.amazon_sku and record.amazon_sku == record.odoo_product_id.default_code:
                    record.match_type = 'sku'
                else:
                    record.match_type = 'none'
            else:
                record.match_type = 'none'
