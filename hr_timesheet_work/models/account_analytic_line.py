from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    work_sheet_id = fields.Many2one('work.sheet', store=True)
    work_id = fields.Many2one('timesheet.work', related='work_sheet_id.work_id', store=True)
    set_start_stop = fields.Boolean(related='work_sheet_id.set_start_stop', string='Set start & stop time', store=False)
    wizard_id = fields.Integer('Wizard', store=True)
