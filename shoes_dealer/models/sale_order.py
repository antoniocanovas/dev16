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

    campaign_id = fields.Many2one('project.project', string="Campaign", store=True, copy=True, tracking=10)
