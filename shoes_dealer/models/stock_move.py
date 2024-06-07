# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    # Comercialmente en cada Albaran quieren saber cuántos pares se han vendido:
    @api.depends("product_id", "quantity_done")
    def _get_shoes_stock_move_pair_count(self):
        for record in self:
            record["pairs_count"] = record.product_id.pairs_count * record.quantity_done

    pairs_count = fields.Integer(
        "Pairs", store=True, compute="_get_shoes_stock_move_pair_count"
    )
