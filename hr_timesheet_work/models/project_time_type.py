from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProjectTimeType(models.Model):
    _inherit = 'project.time.type'

    extra = fields.Boolean('Extra time', store=True)
