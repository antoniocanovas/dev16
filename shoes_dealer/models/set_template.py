# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SetTemplate(models.Model):
    _name = 'set.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Set Template'

    name = fields.Char(string='Nombre', required=True, store=True, copy=True)
    code = fields.Char(string='Code', required=True, store=True, copy=False)
#    main_attribute_id = fields.Many2one('product.attribute', string='Attribute', store=True, required=True, copy=True)
#    main_value_id = fields.Many2one('product.attribute.value', string='Value', store=True, required=True, copy=True)

    attribute_id = fields.Many2one('product.attribute', string='Values Attribute', store=True, required=True, copy=True)
    line_ids = fields.One2many('set.template.line', 'set_id', string='Lines', store=True, copy=True)