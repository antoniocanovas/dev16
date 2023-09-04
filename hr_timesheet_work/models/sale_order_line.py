from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    timesheet_todo_ids = fields.One2many('timesheet.line.todo', 'sale_line_id')
    timesheet_done_ids = fields.One2many('timesheet.line.done', 'sale_line_id')

    @api.depends('timesheet_todo_ids')
    def get_any_todo(self):
        for record in self:
            any_todo = False
            if record.timesheet_todo_ids.ids: any_todo = True
            record.timesheet_todo = any_todo
    timesheet_todo = fields.Boolean(string='To-do', store=False, compute='get_any_todo')


    @api.depends('timesheet_done_ids')
    def get_timesheet_done(self):
        for record in self:
            total = 0
            for li in record.timesheet_done_ids:
                total += li.qty
            record.timesheet_done = total
    timesheet_done = fields.Float(string='Done', store=False, compute='get_timesheet_done')
