from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupTarget(models.Model):
    _name = 'wup.target'
    _description = 'WuP Target '

    name = fields.Char(string='Target', required=True)
