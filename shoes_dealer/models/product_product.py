# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    # Pares por variante de producto, se usará en el cálculo de tarifas y líneas de venta:
    def _get_shoes_product_product_pair_count(self):
        count = 1
        if self.bom_ids.ids:
            count = self.bom_ids[0].pairs_count
        self.pairs_count = count
    pairs_count = fields.Integer('Pairs', store=False, compute='_get_shoes_product_product_pair_count')

