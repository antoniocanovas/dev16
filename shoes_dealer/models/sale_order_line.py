# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Comercialmente en cada pedido quieren saber cuántos pares se han vendido:
    @api.depends('product_id')
    def _get_shoes_sale_line_pair_count(self):
        self.pairs_count = self.product_id.pairs_count
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_sale_line_pair_count')
