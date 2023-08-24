from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    risk_contract_ids = fields.One2many('risk.contract', 'partner_id', string='Risk contracts', store=True, copy=False)

    @api.depends('risk_contract_ids')
    def _get_risk_contract_len(self):
        self.risk_contract_count = len(self.risk_contract_ids.ids)
    risk_contract_count = fields.Integer('Risk contracts', store=False, compute='_get_risk_contract_len')