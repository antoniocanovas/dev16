# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Comercialmente en cada pedido quieren saber cuántos pares se han vendido:
    def _get_shoes_pair_count(self):
        for record in self:
            count = 0
            for li in record.order_line:
                count += li.pairs_count
            record['pairs_count'] = count
    pairs_count = fields.Integer('Pairs', store=False, compute='_get_shoes_pair_count')

    # Evitar vender el mismo producto a dos tiendas que están juntas y son competencia:
    @api.constrains('write_date')
    def _avoid_product_competency_sale_on_confirm(self):
        for record in self:
            competitor_type = self.env.user.company_id.id
            competitors = self.env['res.partner.relation.all'].search(
                [('this_partner_id', '=', record.partner_id.id), ('type_id', '=', competitor_type)]).other_partner_id
            for competitor in competitors:
                for li in record.order_line:
                    sol = self.env['sale.order.line'].search([('order_partner_id', '=', competitor.id),
                                                              ('state', 'in', ['sale', 'done']),
                                                              ('product_id', '=', li.product_id.id)])
                    if sol.id:
                        mensaje = "Producto: " + sol[0].product_id.name + " , incompatible por la venta " + \
                                  sol[0].order_id.name + " al cliente: " + sol[0].order_partner_id.name
                        raise UserError(mensaje)