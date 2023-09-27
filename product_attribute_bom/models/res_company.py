# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    product_attribute_id = fields.Many2one('product.attribute', string='Product attribute bom', store=True)
