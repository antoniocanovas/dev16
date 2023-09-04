from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    work_sheet_id = fields.Many2one('work.sheet', store=True, string='Work Sheet')
