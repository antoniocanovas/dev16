from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    risk_batch_id = fields.Many2one('risk.batch', string='Risk batch', store=True, copy=False)

    @api.depends('payment_state','state','risk_batch_id','partner_id.risk_total')
    def _get_risk_communication_pending(self):
        for record in self:
            pending = True
            if record.payment_state not in ['not_paid','in_payment','partial']:  pending = False
            if record.state not in ['posted']:  pending = False
            if record.risk_batch_id.id: pending = False
            if record.partner_id.credit_limit == 0: pending = False
            record.risk_pending = pending
    risk_pending = fields.Boolean('Risk pending', store=True, default=True,
                                  compute='_get_risk_communication_pending')
