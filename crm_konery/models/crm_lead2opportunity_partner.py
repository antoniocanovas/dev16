from odoo import _, api, fields, models


class CrmLead2opportunityPartner(models.Model):
    _inherit = 'crm.lead2opportunity.partner'

    action = fields.Selection(selection='_get_new_selection')
    @api.model
    def _get_new_selection(self):
        selection = [
        ('text_box', 'Zone de texte à plusieurs lignes'),
        ('char_box', 'Zone de texte sur une seule ligne'),
        ('numerical_box', 'Valeur numérique'),
        ('date', 'Date'),
        ('datetime', 'Date et heure'),
        ('simple_choice', 'Choix multiple : une seule réponse')
        ]
        return selection