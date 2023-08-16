from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    standard_price = fields.Float(tracking=100)
