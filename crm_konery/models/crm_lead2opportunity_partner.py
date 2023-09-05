from odoo import _, api, fields, models


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    action = fields.Selection(default='exist')
