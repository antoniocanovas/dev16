from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.depends('item_ids.product_id')
    def _get_pricelist_products(self):
        products = []
        for li in self.item_ids:
            if li.product_id.id not in products:
                products.append(li.product_id.id)
        self.product_ids = [(6,0,products)]
    product_ids = fields.Many2many('product.product', store=True, compute='_get_pricelist_products')
