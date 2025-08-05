from odoo import api, fields, models

class ProductKitsComponentsGrouped(models.Model):
    _name = 'product.kits.components.grouped'
    _description = 'Grouped Kit Components'
    _auto = False

    mirror_sku = fields.Char('Mirror SKU')
    faucet_sku = fields.Char('Faucet SKU')
    counter_top_sku = fields.Char('Counter Top SKU')
    count = fields.Integer('Count')

    def init(self):
        self._cr.execute("""
            DROP VIEW IF EXISTS product_kits_components_grouped CASCADE;
        """)
        self._cr.execute("""
            CREATE OR REPLACE VIEW product_kits_components_grouped AS (
                SELECT
                    MIN(id) as id,
                    mirror_sku,
                    faucet_sku,
                    counter_top_sku,
                    COUNT(*) as count
                FROM product_kits
                GROUP BY mirror_sku, faucet_sku, counter_top_sku
            )
        """)
