# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _

class TimesheetLineDone(models.Model):
    _inherit = "timesheet.line.done"

    section_id = fields.Many2one('sale.order.line', string='Section', store=True, related='sale_line_id.section_id')
