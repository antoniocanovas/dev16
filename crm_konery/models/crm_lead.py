from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    power_kw = fields.Float(string='Power (kw)', store=True)
