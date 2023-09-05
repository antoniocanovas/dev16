# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ViafirmaNotificationSignature(models.Model):
    _name = 'viafirma.notification'
    _description = 'Viafirma Notifications'

    type = fields.Char('Type')
    name = fields.Char('Name')
    value = fields.Char('Value')
