from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class WorkSheetEmployee(models.Model):
    _name = 'work.sheet.employee'
    _description = 'Work Sheet Employee time'

    employee_id = fields.Many2one('hr.employee', store=True, readonly=True)
    sheet_id = fields.Many2one('work.sheet')
    standard_time = fields.Float('Laboral time', store=True, readonly=True)
    extra_time = fields.Float('Extra time', store=True, readonly=True)
    task_ids = fields.Many2many('project.task', string='Tasks', store=True, readonly=True)
