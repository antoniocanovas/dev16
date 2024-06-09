# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Pablo Archanco Alonso - Aselcis Consulting (http://www.aselcis.com). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from datetime import datetime

from odoo import models, api, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        psi_obj = self.env['product.supplierinfo']
        for l in self.order_line:
            psi = psi_obj.search(
                [('product_tmpl_id', '=', l.product_id.product_tmpl_id.id), ('partner_id', '=', self.partner_id.id)], limit=1)
            if psi:
                psi.write({
                    'discount': l.discount,
                    'price': l.price_unit,
                    'date_start': l.date_price
                })
            else:
                psi_obj.create({
                    'partner_id': self.partner_id.id,
                    'product_tmpl_id': l.product_id.product_tmpl_id.id,
                    'discount': l.discount,
                    'price': l.price_unit,
                    'date_start': l.date_price
                })
            # Precio de coste actualizado siempre a última compra (sólo para cubells, no considera distintas unidades):
#            if l.product_id.uom_po_id == l.product_uom:
#                standard_price = l.price_subtotal / l.product_uom_qty
#                l.product_id.write({'standard_price':standard_price})
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    date_price = fields.Date('Date price', default=datetime.now().date())

#  27/07, da error en línea date= (existe en estándar "purchase" 16, y ahora discount es purchase_discount no como en v11)
#    @api.onchange('product_qty', 'product_uom')
#    def _onchange_quantity(self):
#        res = super(PurchaseOrderLine, self)._onchange_quantity()
#        if not self.product_id:
#            return
#
#        seller = self.product_id._select_seller(
#            partner_id=self.partner_id,
#            quantity=self.product_qty,
#            date=self.order_id.date_order and self.order_id.date_order.date(),
#            uom_id=self.product_uom)
#        if seller:
#            self.discount = seller.discount
#        return res
