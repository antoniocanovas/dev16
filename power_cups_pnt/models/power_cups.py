# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

STATE = [
    ('draft', 'DRAFT'),
    ('done', 'DONE'),
]
class power.cups(models.Model):
    _name = 'power.cups'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Power CUPS'

    name = fields.Char('Name', store=True, copy=True)
    state = fields.Selection(
        selection=STATE,
        string="State",
        default='draft',
        tracking=True,
    )
