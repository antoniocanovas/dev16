from odoo import _, api, fields, models


class CrmLead2opportunityPartner(models.Model):
    _inherit = 'crm.lead2opportunity.partner'

    action = fields.Selection([
        ('exist', 'Link to an existing customer'),
        ('nothing', 'Do not link to a customer')])

#    action = fields.Selection([
#        ('create', 'Create a new customer'),
#        ('exist', 'Link to an existing customer'),
#        ('nothing', 'Do not link to a customer')
#    ], string='Related Customer', compute='_compute_action', readonly=False, store=True, compute_sudo=False)
