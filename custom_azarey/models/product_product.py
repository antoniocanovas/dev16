# Copyright Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, date
class ProductProduct(models.Model):
    _inherit = "product.product"

    # Impedir archivar productos si tienen pedidos de venta:
    pnt_sale_line_ids = fields.One2many('sale.order.line','product_id', string="Sale lines", store=True, copy=False)

    @api.constrains('active')
    def _avoid_archive_sold_products(self):
        for record in self:
            if (record.active == False) and (record.pnt_sale_line_ids.ids):
                raise UserError('Producto con ventas en curso, cancélalas primero.')

    def _delete_product_archived_in_sale_line(self):
        for li in self.pnt_sale_line_ids:
            if li.product_id.id == record.id:
                name = li.product_id.name + ", cantidad: " + str(li.product_uom_qty) + \
                       " => Cancelado el " + str(date.now())
                newnote = env['sale.order.line'].create(
                    {'display_type': 'line_note', 'name': name, 'order_id': li.order_id.id})
                li.unlink()