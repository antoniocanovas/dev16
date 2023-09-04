from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'account.analytic.tag'

    timesheet_hidden = fields.Boolean(string='Hidden in Timesheet', help='If true, this tag will be hidden in lot work timesheets creation')
