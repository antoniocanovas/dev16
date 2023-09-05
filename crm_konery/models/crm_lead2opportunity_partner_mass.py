from odoo import _, api, fields, models


class CrmLead2opportunityPartnerMass(models.Model):
    _inherit = 'crm.lead2opportunity.partner.mass'

    action = fields.Selection(selection_add=[
        ('each_exist_or_create', 'Use existing partner or create'),
    ], string='Related Customer', ondelete={
        'each_exist_or_create': lambda recs: recs.write({'action': 'exist'}),
    })