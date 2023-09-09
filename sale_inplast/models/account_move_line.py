from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_ids = fields.Many2many('product.product', store=False, string='Pricelist products',
                                   related='pricelist_id.product_ids')
