# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class PowerCUPS(models.Model):
    _name = 'power.cups'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Power CUPS'

    name = fields.Char('Name', store=True, copy=True, required=True)
    pnt_state = fields.Selection(
        selection=[('draft','Draft'),('done','Done')],
        string="State",
        default='draft',
        tracking=True,
    )

    pnt_partner_id = fields.Many2one('res.partner', string='Contact', store=True, copy=True)
    pnt_dealer_id = fields.Many2one('res.partner', string='Dealer', store=True, copy=True)
    pnt_marketeer_id = fields.Many2one('res.partner', string='Marketeer', store=True, copy=True)