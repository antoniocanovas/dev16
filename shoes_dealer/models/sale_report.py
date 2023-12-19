# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class SaleReport(models.Model):
    _inherit = "sale.report"


    color_attribute_id = fields.Many2one('product.attribute.value', string='Color', store=True,
                                         related='product_id.color_attribute_id')

    size_attribute_id = fields.Many2one('product.attribute.value', string='Size', store=True,
                                         related='product_id.size_attribute_id')

    @api.depends('product_id')
    def _get_shoes_pair_count(self):
        for record in self:
            pairs_count = 1
            if record.product_id.pairs_count: pairs_count = record.product_id.pairs_count
            record['pairs_count'] = pairs_count * record.product_uom_qty
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_pair_count')
