# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ViafirmaSignature(models.Model):
    _name = 'viafirma.signature'
    _description = 'Viafirma Signature'

    type = fields.Char('Type')
    name = fields.Char('Name')
    value = fields.Char('Value')
