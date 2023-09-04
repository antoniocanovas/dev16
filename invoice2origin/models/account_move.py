# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice2origin_previous_ids =  fields.Many2many(
        string='Facturas FEO',
        comodel_name='account.move',
        relation='invoice2origin_move_rel',
        column1='move_id',
        column2='previous_invoice_id',
    )