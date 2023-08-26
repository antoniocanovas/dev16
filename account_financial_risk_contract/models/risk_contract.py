from odoo import _, api, fields, models
from datetime import date
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class RiskContract(models.Model):
    _name = 'risk.contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Risk Contracts'

    STATE = [('draft', 'Draft'),
             ('waiting', 'Waiting'),
             ('done', 'Done'),
             ('refused', 'Refused'),
             ]

    name = fields.Char(string='Name', required=True, tracking=100)
    partner_id = fields.Many2one('res.partner', string='Partner', store=True, copy=True, required=True, tracking=100)
    date_begin = fields.Date('Date begin', store=True, copy=False, tracking=100)
    date_end = fields.Date('Date end', store=True, copy=False, tracking=100)
    level = fields.Char('Level', store=True, copy=True, tracking=100)
    percentage = fields.Float('Coberture', store=True, copy=True, tracking=100)
    supplier_id = fields.Many2one('res.partner', string='Supplier', store=True, copy=True, required=True, tracking=100)
    demand = fields.Monetary('Demand', store=True, copy=True, required=True)
    amount = fields.Monetary('Amount', store=True, copy=True, tracking=100)
    currency_id = fields.Many2one('res.currency', store=True, default=1, required=True)
    active = fields.Boolean('Active', store=True, copy=False, default=True, tracking=100)
    state = fields.Selection(selection=STATE, string="State", store=True, copy=False, default='draft', tracking=100)
    description = fields.Text('Notes', store=True, copy=False)

    def update_risk_partner(self):
        if self.date_end > date.today():
            self.partner_id.credit_limit = self.amount
        else:
            raise UserError('Expiration date must be after today')