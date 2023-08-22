# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    svl_id = fields.Many2one('stock.valuation.layer', string='Stock Valuation Layer', store="True",)
