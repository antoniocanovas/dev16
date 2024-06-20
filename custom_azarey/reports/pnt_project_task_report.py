
from collections import defaultdict
import math
from odoo.exceptions import UserError

from odoo import _, api, fields, models
from odoo.exceptions import UserError

def _prepare_data(env, data):
    if data.get('active_model') == 'project.task':
        task = env['project.task']
    else:
        raise UserError(_('Model not defined, Please contact your administrator.'))

    task_ids = data.get('task_ids')
    tasks = task.search([('id', 'in', task_ids)], order='name desc')
    tasks_number = len(task_ids)
    layout_wizard = env['project.task.report.wizard'].browse(data.get('layout_wizard'))
    if layout_wizard.pnt_columns == 2:
        raw_rows = tasks_number / layout_wizard.pnt_columns
        rows = math.ceil(raw_rows)
    else:
        rows = len(task_ids)

    if not layout_wizard:
        return {}

    return {
        'tasks': tasks,
        'tasks_number': tasks_number,
        'rows': rows,
        'columns': layout_wizard.pnt_columns,
        #'page_numbers': (total - 1) // (layout_wizard.pnt_rows * layout_wizard.pnt_columns) + 1,
    }

class ProjectTaskReport(models.AbstractModel):
    _name = 'report.custom_azarey.project_task_report'
    _description = 'Reporting engine for project task'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)
