from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RiskBatch(models.Model):
    _name = 'risk.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Risk invoices batch'

    STATE = [('draft', 'Draft'),
             ('done', 'Done'),
             ]

    name = fields.Char(string='Name', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', store=True, copy=True, required=True)
    date = fields.Date('Date', store=True, copy=False)
    currency_id = fields.Many2one('res.currency', store=True, default=1, required=True)
    state = fields.Selection(selection=STATE, string="State", store=True, copy=False, default='draft')
    description = fields.Text('Notes', store=True, copy=False)
    invoice_ids = fields.Many2many('account.move', store=True)

    def _get_invoices_net_amount(self):
        amount = 0
        for li in self.invoice_ids:
            amount += li.amount_untaxed_signed
        self.amount = amount
    amount = fields.Monetary('Amount', store=False, copy=True, compute='_get_invoices_net_amount')

    @api.depends('invoice_ids')
    def _update_invocice_risk_batch_id(self):
        for record in self:
            invoices = self.env['account.move'].search([('risk_batch_id','=',record.id)])
            for li in invoices:
                if li.id not in record.invoice_ids.ids:
                    li['risk_batch_id'] = False
            for li in record.invoice_ids:
                if li.id != record.id:
                    li['risk_batch_id'] = record.id
