# Copyright Punt Sistemes SL - PUNT

from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date

class ProductProduct(models.Model):
    _inherit = "product.product"

    # Impedir archivar productos si tienen pedidos de venta:
    pnt_sale_line_ids = fields.One2many('sale.order.line','product_id', string="Sale lines", store=True, copy=False)

    @api.constrains('active')
    def _avoid_archive_sold_products(self):
        for record in self:
            if (record.active == False) and (record.pnt_sale_line_ids.ids):
                raise UserError('Remove sale lines before archiving !!')
            if (record.active == False) and (record.purchase_order_line_ids.ids):
                raise UserError('Remove purchase lines before archiving !!')

    def delete_product_archived_in_sale_line(self):
        for li in self.pnt_sale_line_ids:
            if li.product_id.id == self.id:
                if li.state == 'done':
                    message = 'Confirmed sales order must be cancelled and set to RESERVATION before: ' + li.order_id.name
                    raise UserError(message)
                else:
                    name = li.product_id.name + ", cantidad: " + str(li.product_uom_qty) + \
                           " => Cancelado el " + str(date.today())
                    newnote = self.env['sale.order.line'].create(
                        {'display_type': 'line_note', 'name': name, 'order_id': li.order_id.id})
                    li.unlink()