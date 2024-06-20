# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    pnt_print_reference_invoice = fields.Boolean(string='Print Reference on invoice', default=False)
