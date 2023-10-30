# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    # Pares por variante de producto, se usará en el cálculo de tarifas y líneas de venta:
    def _get_shoes_product_product_pair_count(self):
        for record in self:
            count = 0
            if record.bom_ids.ids:
                bom = self.env['mrp.bom'].search([('product_id','=',record.id)]).sorted(key=lambda r: r.sequence)[0]
                for li in bom.bom_line_ids:
                    count += li.product_qty
            else: count = 1
            record['pairs_count'] = count
    pairs_count = fields.Integer('Pairs', store=False, compute='_get_shoes_product_product_pair_count')

