# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _

class ProjectTask(models.Model):
    _inherit = ['project.task']

    outfit = fields.Char('Outfit', store=True, copy=True)

    def action_open_task_report_layout(self):
        return {
            'name': _("Report Wizard"),
            'view_mode': 'form',
            'view_id': self.env.ref('custom_azarey.project_task_wizard_view').id,
            'view_type': 'form',
            'res_model': 'project.task.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            # 'domain': '[if you need]',
            'context': {'default_pnt_project_id': self.project_id.id,
                        'default_pnt_task_ids': self.ids,
                        }
        }
