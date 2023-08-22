# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    analytic_line_ids = fields.One2many('account.analytic.line', 'svl_id', string='Analytic Lines', store="True",)
