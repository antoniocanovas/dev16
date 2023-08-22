from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    wup_line_id = fields.Many2one('wup.line', string='Wup Line', store=True, copy=True)
