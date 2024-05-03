from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class PartnerCredentialType(models.Model):
    _name = 'partner.credential.type'
    _description = 'Partner credential type'

    name = fields.Char(string='Name', required=True)
    department_ids = fields.Many2many("hr.department", string="Departments")
