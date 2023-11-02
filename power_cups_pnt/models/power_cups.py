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

    pnt_kw_fw       = fields.Float('Photovoltaic (kw)', store=True, copy=True)
    pnt_kw_inverter = fields.Float('Inverter (kw)', store=True, copy=True)
    pnt_kw_battery  = fields.Float('Battery (kw)', store=True, copy=True)
    pnt_kw_contract = fields.Float('Contract (kw)', store=True, copy=True)
    pnt_kw_access   = fields.Float('Access (kw)', store=True, copy=True)
    pnt_isolated    = fields.Boolean('Isolated', store=True, copy=True)

    pnt_target_type = fields.Selection(
        selection=[('acc','Autoconsumo con compensación'),
                   ('asc','Autoconsumo sin compensación'),
                   ('venta','Venta a red')],
        string="Customer type",
        default='asc',
    )

    pnt_customer_type = fields.Selection(
        selection=[('person','Person'),('company','Company'),('community','Community'),
                   ('shared','Shared'),('residential','Residential')],
        string="Customer type",
        default='person',
    )

    pnt_surface_type = fields.Selection(
        selection=[('roof','Roof'),('rustic','Rustic'),('flat','Flat'),('wall','Wall')],
        string="Surface",
        default='roof',
        tracking=True,
    )

