from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    pnt_power_cups_id = fields.Many2one('power.cups', string='CUPS', store=True, copy=False)
    pnt_partner_id = fields.Many2one('res.partner', string='Customer', store=False, related='pnt_power_cups_id.pnt_partner_id')
    pnt_dealer_id = fields.Many2one('res.partner', string='Dealer', store=False, related='pnt_power_cups_id.pnt_dealer_id')
    pnt_marketeer_id = fields.Many2one('res.partner', string='Marketeer', store=False, related='pnt_power_cups_id.pnt_marketeer_id')
    pnt_state = fields.Selection(
        selection=[('draft','Draft'),('done','Done')],
        string='State', related='pnt_power_cups_id.pnt_state', store=False)

    pnt_kw_fw       = fields.Float('Photovoltaic (kw)', store=True, readonly=False, related='pnt_power_cups_id.pnt_kw_fw')
    pnt_kw_inverter = fields.Float('Inverter (kw)', store=True, readonly=False, related='pnt_power_cups_id.pnt_kw_inverter')
    pnt_kw_battery  = fields.Float('Battery (kw)', store=True, readonly=False, related='pnt_power_cups_id.pnt_kw_battery')
    pnt_isolated    = fields.Boolean('Isolated', store=True, readonly=False, related='pnt_power_cups_id.pnt_isolated')

    pnt_electric_type = fields.Selection(
        selection=[('mono','Monofásica'),
                   ('tri','Trifásica')],
        string="Electricity",
        default='mono',
        store=True, readonly=False,
        related='pnt_power_cups_id.pnt_electric_type',
    )

    pnt_target_type = fields.Selection(
        selection=[('acc','Autoconsumo con compensación'),
                   ('asc','Autoconsumo sin compensación'),
                   ('venta','Venta a red')],
        string="Customer type",
        store=True, readonly=False,
        related='pnt_power_cups_id.pnt_target_type',
    )

    pnt_customer_type = fields.Selection(
        selection=[('person','Person'),('company','Company'),('community','Community'),
                   ('shared','Shared'),('residential','Residential')],
        string="Customer type",
        store=True, readonly=False,
        related='pnt_power_cups_id.pnt_customer_type',
    )

    pnt_surface_type = fields.Selection(
        selection=[('roof','Roof'),('rustic','Rustic'),('flat','Flat'),('wall','Wall')],
        string="Surface",
        store=True, readonly=False,
        related='pnt_power_cups_id.pnt_surface_type',
    )
