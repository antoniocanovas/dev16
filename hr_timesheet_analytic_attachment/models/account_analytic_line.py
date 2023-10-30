# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _

class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def get_worksheet_attachment(self):
        data = self.env['ir.attachment'].search([('res_model', '=', 'work.sheet'), ('res_id', '=', self.work_sheet_id.id)])
        self.worksheet_attachment_ids = [(6, 0, data.ids)]
    worksheet_attachment_ids = fields.Many2many(comodel_name='ir.attachment',
                                           relation='work_sale_attachment_rel',
                                           column1='analytic_id',
                                           column2='attachment_id',
                                           store=False,
                                           compute='get_worksheet_attachment',
                                           string='Archivos')
