# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas & PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    retention_enable = fields.Boolean('Retention', default=False)
    retention_description = fields.Char('Description')
    retention_type = fields.Selection([('manual', 'Manual'),
                                       ('percent_net', 'Percent net'),
                                       ('percent_gross', 'Percent Gross')], string='Type')
    retention_percent = fields.Float('Percent')

    @api.depends('retention_enable', 'retention_type', 'retention_percent', 'amount_untaxed','amount_total')
    def _get_retention_amount(self):
        for record in self:
            retention = record.retention_amount
            if (record.retention_enable == True) and (record.retention_type == 'percent_net'):
                retention = record.amount_untaxed * (record.retention_percent/100)
            elif (record.retention_enable == True) and (record.retention_type == 'percent_gross'):
                retention = record.amount_total * (record.retention_percent/100)
            record.retention_amount = retention
    retention_amount = fields.Monetary(string="Amount retained", store=True,
                                       readonly=False, compute=_get_retention_amount)

    @api.depends('retention_enable', 'retention_amount', 'amount_untaxed','amount_total')
    def _get_retention_excluded(self):
        self.retention_excluded = self.amount_total - self.retention_amount
    retention_excluded = fields.Monetary(string="Retention excluded", store=False, compute=_get_retention_excluded)
