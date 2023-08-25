from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    risk_batch_id = fields.Many2one('risk.batch', string='Risk batch', store=True, copy=False)

    @api.depends('payment_status','state', 'risk_batch_id')
    def _get_risk_communication_pending(self):
        pending = True
        if self.payment_state not in ['not_paid','in_payment','partial']:  pending = False
        if self.state not in ['posted']:  pending = False
        if self.risk_batch_id.id: pending = False
        self.risk_pending = pending
    risk_pending = fields.Boolean('Risk pending', store=True, default=True,
                                  compute='_get_risk_communication_pending')
