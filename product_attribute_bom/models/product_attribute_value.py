# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    set_template_id = fields.Many2one('set.template', string='Set template', store=True, copy=False)
    
    def _get_company_bom_attribute_id(self):
        self.company_attribute_bom_id = self.env.user.company_id.product_attribute_id.id
    company_attribute_bom_id = fields.Many2one('product.attribute', string='Company bom attribute',
                                               store=False, compute='_get_company_bom_attribute_id')
