from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupQuality(models.Model):
    _name = 'wup.quality'
    _description = 'WuP Quality '

    name = fields.Char(string='Quality', required=True)
