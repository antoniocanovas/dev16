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

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['color_attribute_id'] = "s.color_attribute_id"
        res['size_attribute_id'] = "s.size_attribute_id"
        res['pairs_count'] = "s.pairs_count"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
        s.color_attribute_id,
        s.size_attribute_id,
             s.pairs_count"""
        return res