# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Comercialmente en cada pedido quieren saber cuántos pares se han vendido:
    @api.depends('product_id', 'product_uom_qty')
    def _get_shoes_sale_line_pair_count(self):
        for record in self:
            record['pairs_count'] = record.product_id.pairs_count * record.product_uom_qty
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_sale_line_pair_count')

    campaign_id = fields.Many2one('project.project', string='Campaign (borrar)', related='order_id.campaign_id')
    shoes_campaign_id = fields.Many2one('project.project', string='Campaign', related='order_id.shoes_campaign_id')

    # Precio por par según tarifa:
    @api.depends('product_id','price_unit')
    def _get_shoes_pair_price(self):
        for record in self:
            total = 0
            if record.pairs_count != 0: total = record.price_subtotal / record.pairs_count
            record['pair_price'] = total
    pair_price = fields.Float('Pair price', store=True, compute='_get_shoes_pair_price')

    product_saleko_id = fields.Many2one('product.product', string='Product KO', store=True, copy=True)

    @api.onchange('product_saleko_id')
    def change_saleproductok_2_saleproductko(self):
        self.product_id = self.product_saleko_id.id