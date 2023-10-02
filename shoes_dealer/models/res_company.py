# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    bom_attribute_id = fields.Many2one('product.attribute', string='Set attribute', store=True, required=True)
    size_attribute_id = fields.Many2one('product.attribute', string='Size attribute', store=True, required=True)
    color_attribute_id = fields.Many2one('product.attribute', string='Color attribute', store=True, required=True)