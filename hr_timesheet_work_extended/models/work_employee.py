from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WorkEmployee(models.Model):
    _name = 'work.employee'
    _description = 'WorkEmployee'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    work_id = fields.Many2one('timesheet.work', 'Work')
    function_ids = fields.Many2many('hr.job')

