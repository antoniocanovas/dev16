from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    employee_id = fields.Many2one('hr.employee', related='location_id.employee_id')
    department_id = fields.Many2one('hr.department', related='location_id.department_id')
