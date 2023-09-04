from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    quant_ids = fields.One2many('stock.quant', 'employee_id', store=True, readonly=True)

