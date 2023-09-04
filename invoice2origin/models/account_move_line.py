# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoice2origin_qty = fields.Float(string='Origin Qty')
    invoice2origin_amount_subtotal = fields.Monetary(string='Origin Subtotal', store=False, compute="get_price")

    def get_price(self):
        for record in self:
            total = 0
            if record.quantity != 0:
                total = (record.price_subtotal / record.quantity) * record.invoice2origin_qty
            record.invoice2origin_amount_subtotal = total
