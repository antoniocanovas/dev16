from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(tracking=100)
