from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pnt_power_cups_id = fields.Many2one('power.cups', string='CUPS', store=True, copy=False)
    pnt_partner_id = fields.Many2one('res.partner', string='Customer', store=False, related='pnt_power_cups_id.pnt_partner_id')
    pnt_dealer_id = fields.Many2one('res.partner', string='Dealer', store=False, related='pnt_power_cups_id.pnt_dealer_id')
    pnt_marketeer_id = fields.Many2one('res.partner', string='Marketeer', store=False, related='pnt_power_cups_id.pnt_marketeer_id')
    pnt_state = fields.Selection(string='State', related='pnt_power_cups_id.pnt_state', store=False)



