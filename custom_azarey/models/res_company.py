# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    competence_relation_id = fields.Many2one('res.partner.relation.type', string='Competence relation', store=True)
