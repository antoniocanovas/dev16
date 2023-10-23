# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ProductTag(models.Model):
    _inherit = 'product.tag'

    pricelist_print = fields.Boolean('Pricelist printed', store=True, copy=True)
    pricelist_image_type = fields.Binary('Image', store=True, copy=False)
    pricelist_image_feature = fields.Binary('Feature', store=True, copy=False)
