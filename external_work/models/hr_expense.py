from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class HRExpense(models.Model):
    _inherit = 'hr.expense'

    external_work_id = fields.Many2one('external.work', store=True, string="External Work")
