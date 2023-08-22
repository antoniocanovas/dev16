# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WupSolWizard(models.TransientModel):
    _name = "wup.saleline.wizard"
    _description = "WUP New Sale Order Line add Wizard"

    sale_id = fields.Many2one('sale.order')
    analytic_line_ids = fields.Many2many('account.analytic.line', store=True)
    product_consumed_ids = fields.Many2many('account.analytic.line', related='sale_id.product_consumed_ids')

    def create_sale_order_lines(self):
        picking = 0
        for aal in self.analytic_line_ids:
            svl = self.env['stock.valuation.layer'].search([('analytic_id', '=', aal.id)])
            sm = svl.stock_move_id
            if (svl.id) and not (sm.sale_line_id.id):
                newsol = self.env['sale.order.line'].create({
                    'order_id': self.sale_id.id,
                    'product_id': sm.product_id.id,
                    'product_uom_qty': sm.quantity_done,
                })
                picking = newsol.move_ids[0].picking_id
                for li in newsol.move_ids:
                    li['state'] = 'draft'
                    li.unlink()
                sm['sale_line_id'] = newsol.id
                newsol['qty_delivered'] = sm.quantity_done
        if (picking != 0) and (not picking.move_ids_without_package.ids):
            picking['state'] = 'cancel'
