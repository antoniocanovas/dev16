from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class PartnerCredentialCategory(models.Model):
    _name = 'partner.credential.category'
    _description = 'Partner credential category'

    name = fields.Char(string='Name', required=True)
    department_ids = fields.Many2many("hr.department", string="Departments")
