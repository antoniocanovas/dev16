# Copyright Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    # Impedir archivar productos si tienen pedidos de venta:
    pnt_sale_line_ids = fields.One2many('sale.order.line','product_id', string="Sale lines", store=True, copy=False)

    @api.constrains('active')
    def _avoid_archive_sold_products(self):
        for record in self:
            if (record.active == False) and (record.pnt_sale_line_ids.ids):
                raise UserError('Producto con ventas en curso, cancélalas primero.')