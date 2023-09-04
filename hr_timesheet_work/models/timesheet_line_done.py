# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _


class TimesheetLineDone(models.Model):
    _name = "timesheet.line.done"
    _description = "Timesheet Line Done"

    todo_id = fields.Many2one('timesheet.line.todo', string='Item', required=True)
    qty = fields.Float(string='Quantity', required="1")
    uom_id = fields.Many2one('uom.uom', store=True, string='UOM', related='todo_id.uom_id')
    work_sheet_id = fields.Many2one('work.sheet', string='Sheet', store=True)
    sale_line_id = fields.Many2one('sale.order.line', string='Sale line', store=True, related='todo_id.sale_line_id')
    sale_id = fields.Many2one('sale.order', string='Sale order', store=True, related='todo_id.sale_id')
    date = fields.Date(string='Date', store=True, related='work_sheet_id.date' )
    time_elapsed = fields.Float('Time', store=True)
    work_id = fields.Many2one('timesheet.work', related='work_sheet_id.work_id', store=True)
    product_id = fields.Many2one('product.product', related='todo_id.product_id', store=True)
    employee_ids = fields.Many2many('hr.employee')

    @api.depends('todo_id')
    def get_done_name(self):
        for record in self:
            record.name = record.todo_id.name
    name = fields.Char(string='Description', compute='get_done_name', readonly=False, store=True, required="1")

    @api.depends('employee_ids','qty','time_elapsed')
    def get_performance(self):
        for record in self:
            performance = 0
            employees = len(record.employee_ids)
            if (employees == 0): employees = 1
            if (employees > 0) and (record.time_elapsed > 0):
                performance = record.qty / (employees * record.time_elapsed)
            record.performance = performance
    performance = fields.Float('Units/hour', store=False, compute='get_performance')