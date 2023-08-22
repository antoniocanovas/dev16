from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    wup_line_id = fields.Many2one('wup.line', string='Wup Line', store=True, copy=True, related='task_id.wup_line_id')
