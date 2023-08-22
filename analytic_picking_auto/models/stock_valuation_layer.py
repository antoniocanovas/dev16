# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    analytic_id = fields.Many2one('account.analytic.line', string='Analytic Line', store="True",)
