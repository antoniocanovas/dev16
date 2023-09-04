from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    timesheet_done_ids = fields.One2many('timesheet.line.done', 'sale_id')

    @api.depends('timesheet_done_ids')
    def get_timesheet_line_done_count(self):
        for record in self:
            record.timesheet_done_count = len(record.timesheet_done_ids)
    timesheet_done_count = fields.Integer(string='Lines Done', store=False, compute='get_timesheet_line_done_count')
