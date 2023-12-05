
from odoo import _, api, fields, models



class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add = [('5x6', '5 x 6')],  default='5x6', ondelete={'5x6': 'set default'})

