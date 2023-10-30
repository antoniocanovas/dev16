from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    tracking_date = fields.Datetime('Tracking date', store=True, copy=False)
