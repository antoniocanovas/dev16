from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'hr.expense'

    work_sheet_id = fields.Many2one('work.sheet', store=True)
