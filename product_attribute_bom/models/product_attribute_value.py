# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    set_template_id = fields.Many2one('set.template', string='Set template', store=True, copy=False)
