
from odoo import _, api, fields, models
from odoo.exceptions import UserError



REPORT_TYPE = [
    ('2x5', '2 x 5'),
    ('1x2', '1 x 2'),
]

class ProjectTaskReportWizard(models.TransientModel):
    _name = 'project.task.report.wizard'
    _description = 'Reporting engine for project task'

    pnt_project_task_report_template = fields.Selection(
        selection=REPORT_TYPE,
        string="Report Type",
        default='2x5',)
    pnt_project_id = fields.Many2one('project.project', string="Product pricelist")
    pnt_task_ids = fields.Many2many('project.task', string="Tasks")
    pnt_rows = fields.Integer(compute='_compute_dimensions')
    pnt_columns = fields.Integer(compute='_compute_dimensions')

    @api.depends('pnt_project_task_report_template')
    def _compute_dimensions(self):
        for wizard in self:
            if 'x' in wizard.pnt_project_task_report_template:
                columns, rows = wizard.pnt_project_task_report_template.split('x')[:2]
                wizard.pnt_columns = int(columns)
                wizard.pnt_rows = int(rows)
            else:
                wizard.pnt_columns, wizard.pnt_rows = 1, 1

    def _prepare_report_data(self):

        xml_id = 'custom_azarey.pnt_project_task_report'

        # Build data to pass to the report
        data = {
            'active_model': 'project.task',
            'task_ids': self.pnt_task_ids.ids,
            'layout_wizard': self.id,
        }
        return xml_id, data

    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(
                _('Unable to find report template for %s format', self.pnt_project_task_report_template))
        report_action = self.env.ref(xml_id).report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action