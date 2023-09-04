# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice2origin_title = fields.Text(string='Obra F.E.O.')



