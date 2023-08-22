from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupLine(models.Model):
    _inherit = 'wup.line'

    fix_price_unit_cost = fields.Boolean(
        string='Fix Cost',
        help="If active, this price will not be recalculated with real product cost",
        store=True,
        readonly=False,
    )

    fix_price_unit_sale = fields.Boolean(
        string='Fix Sale',
        help="If active this price will not be recalculated with margin of special discounts",
        store=True,
        readonly=False,
    )
