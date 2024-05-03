# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredentialsFields(models.Model):
    _inherit = "res.partner"

    def _get_credentials(self):
        results = self.env["partner.credentials"].search([("partner_id", "=", self.id)])
        self.credentials_count = len(results)

    credentials_count = fields.Integer(
        "Credentials", compute=_get_credentials, store=False
    )

    def action_view_credentials(self):
        action = self.env.ref("partner_credential.action_partner_credential").read()[
            0
        ]
        return action
