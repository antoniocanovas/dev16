# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class PowerCUPS(models.Model):
    _name = 'power.cups'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Power CUPS'

    name = fields.Char('Name', store=True, copy=True, required=True)
    state = fields.Selection(
        selection=[('draft','DRAFT'),('done','DONE')],
        string="State",
        default='draft',
        tracking=True,
    )

    partner_id = fields.Many2one('res.partner', string='Contact', store=True, copy=True)
    dealer_id = fields.Many2one('res.partner', string='Dealer', store=True, copy=True)
    marketeer_id = fields.Many2one('res.partner', string='Marketeer', store=True, copy=True)