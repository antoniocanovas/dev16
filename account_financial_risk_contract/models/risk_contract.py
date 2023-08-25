from odoo import _, api, fields, models

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

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', store=True, copy=True, required=True)
    date_begin = fields.Date('Date begin', store=True, copy=False)
    date_end = fields.Date('Date end', store=True, copy=False)
    level = fields.Char('Level', store=True, copy=True)
    percentage = fields.Float('Coberture', store=True, copy=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', store=True, copy=True, required=True)
    demand = fields.Monetary('Demand', store=True, copy=True, required=True)
    amount = fields.Monetary('Amount', store=True, copy=True)
    currency_id = fields.Many2one('res.currency', store=True, default=1, required=True)
    active = fields.Boolean('Active', store=True, copy=False, default=True)
    state = fields.Selection(selection=STATE, string="State", store=True, copy=False, default='draft')
    description = fields.Text('Notes', store=True, copy=False)