from odoo import _, api, fields, models

class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    prueba = fields.Char('Prueba')
    action_konery = fields.Selection([
        ('exist', 'Link to an existing customer'),
        ('nothing', 'Do not link to a customer')
    ], string='Related Customer', compute='_compute_action', readonly=False, store=True, compute_sudo=False)

#    action = fields.Selection([
#        ('create', 'Create a new customer'),
#        ('exist', 'Link to an existing customer'),
#        ('nothing', 'Do not link to a customer')
#        ])
    @api.model
    def _get_new_selection(self):
        selection = [
        ('exist', 'Link to an existing customer'),
        ('nothing', 'Do not link to a customer')
        ]
        return selection

#         ('create', 'Create a new customer'),