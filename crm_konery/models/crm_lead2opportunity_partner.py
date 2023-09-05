from odoo import _, api, fields, models


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    action = fields.Selection(selection='_get_new_selection')
    @api.model
    def _get_new_selection(self):
        selection = [
        ('exist', 'Link to an existing customer'),
        ('nothing', 'Do not link to a customer')
        ]
        return selection

#         ('create', 'Create a new customer'),