# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    # Pares por variante de producto, se usará en el cálculo de tarifas y líneas de venta:
    def _get_shoes_product_product_pair_count(self):
        for record in self:
            count = 1
            bom = self.env['mrp.bom'].search([('product_id','=',self.id)])
            if bom.ids:
                count = bom[0].pairs_count
            record['pairs_count'] = count
    pairs_count = fields.Integer('Pairs', store=False, compute='_get_shoes_product_product_pair_count')

