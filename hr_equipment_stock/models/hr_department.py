from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    quant_ids = fields.One2many('stock.quant', 'department_id')


