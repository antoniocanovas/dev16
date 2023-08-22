# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    analytic_line_ids = fields.Many2many('account.analytic.line', string='Analytic Lines', store="True",)
