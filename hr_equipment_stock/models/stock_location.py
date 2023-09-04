from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    employee_id = fields.Many2one('hr.employee')
    department_id = fields.Many2one('hr.department')

