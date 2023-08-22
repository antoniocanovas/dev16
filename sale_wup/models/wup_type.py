from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupType(models.Model):
    _name = 'wup.type'
    _description = 'WUP Type '

    name = fields.Char(string='Type', required=True)
