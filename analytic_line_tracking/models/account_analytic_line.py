# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = ['account.analytic.line', 'mail.thread', 'mail.activity.mixin']


    name = fields.Char(tracking=True)
    date = fields.Date(tracking=True)
    amount = fields.Monetary(tracking=True)
    unit_amount = fields.Float(tracking=True)
    account_id = fields.Many2one(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    user_id = fields.Many2one(tracking=True)
    employee_id = fields.Many2one(tracking=True)
    product_id = fields.Many2one(tracking=True)

