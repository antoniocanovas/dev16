# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.tools import html2plaintext


class MailMessage(models.Model):
    _inherit = "mail.message"

    # Para sacar informes exportados impresos para el jefe (notas como texto):
    def _get_body_text(self):
        for record in self:
            record['pnt_bodytext'] = html2plaintext(record.body)
    pnt_bodytext = fields.Text(string="Body text", compute="_get_body_text")
