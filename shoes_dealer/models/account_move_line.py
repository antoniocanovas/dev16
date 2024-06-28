# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Comercialmente en cada pedido quieren saber cuántos pares se han facturado:
    @api.depends('product_id', 'quantity')
    def _get_shoes_invoice_line_pair_count(self):
        for record in self:
            record['pairs_count'] = record.product_id.pairs_count * record.quantity
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_invoice_line_pair_count')

    # Precio por par según tarifa:
    @api.depends('product_id','price_unit')
    def _get_shoes_invoice_pair_price(self):
        for record in self:
            total = 0
            if record.pairs_count != 0: total = record.price_subtotal / record.pairs_count
            record['pair_price'] = total
    pair_price = fields.Float('Pair price', store=True, compute='_get_shoes_invoice_pair_price')

    color_attribute_id = fields.Many2one('product.attribute.value', string='Color',
                                         store=True,
                                         related='product_id.color_attribute_id')

    size_attribute_id = fields.Many2one('product.attribute.value', string='Size',
                                         store=True,
                                         related='product_id.size_attribute_id')

    shoes_campaign_id = fields.Many2one('project.project', string='Shoes Campaign',
                                        store=True,
                                        related='product_id.shoes_campaign_id')
    shoes_model_id = fields.Many2one('product.template', store=True, related='product_id.shoes_model_id')
    exwork_single_euro = fields.Monetary(related="shoes_model_id.exwork_single_euro")

    @api.depends('price_subtotal', 'cost_price')
    def _get_shoes_margin(self):
        for record in self:
            record['shoes_margin'] = record.price_subtotal - record.cost_price

    shoes_margin = fields.Monetary('Margin', compute='_get_shoes_margin')

    @api.depends('shoes_margin', 'pairs_count')
    def _get_shoes_pair_margin(self):
        for record in self:
            shoes_pair_margin = record.shoes_pair_margin
            if record.pairs_count != 0:
                shoes_pair_margin = record.shoes_margin / record.pairs_count
            record['shoes_pair_margin'] = shoes_pair_margin

    shoes_pair_margin = fields.Monetary('Pair margin', compute='_get_shoes_pair_margin')


    @api.depends("price_unit")
    def _get_pair_price_sale(self):
        for record in self:
            price_unit = record.price_unit
            if (record.pairs_count != 0) and (record.quantity):
                price_unit = price_unit / record.pairs_count * record.quantity
            record['pair_price_sale'] = price_unit
    pair_price_sale = fields.Monetary("Pair price sale", compute="_get_pair_price_sale")

    @api.depends('exwork_single_euro', 'pairs_count')
    def _get_cost_price(self):
        for record in self:
            record.cost_price = record.pairs_count * record.exwork_single_euro

    cost_price = fields.Float("Cost price", compute="_get_cost_price")
