# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    # Campo para la migración, mejor que se acostumbren a no usarlo, o poner el ID en la vista.
    code = fields.Integer('Code', store=True, copy=False)