from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    risk_batch_id = fields.Many2one('risk.batch', string='Risk batch', store=True, copy=False)
