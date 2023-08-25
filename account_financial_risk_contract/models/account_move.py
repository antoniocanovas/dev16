from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    risk_batch_id = fields.Many2one('risk.batch', string='Risk barch', store=True, copy=False)
