from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    section_id = fields.Many2one('sale.order.line', related='sale_line_id.section_id', string='Section')
