from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupStyle(models.Model):
    _name = 'wup.style'
    _description = 'WuP Style '

    name = fields.Char(string='Style', required=True)
