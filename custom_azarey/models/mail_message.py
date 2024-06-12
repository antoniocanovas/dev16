# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from bs4 import BeautifulSoup
from odoo.tools import (html2plaintext, cleanup_xml_node)


class MailMessage(models.Model):
    _inherit = "mail.message"

    # Para sacar informes exportados impresos para el jefe (notas como texto):
    pnt_bodytext = fields.Text(
        string="Body text",
        compute="_get_body_text",
    )

    def _get_body_text(self):
        for record in self:
            text = html2plaintext(record.body)
#            text = BeautifulSoup(record.body, 'html.parser').get_text()
            record['pnt_bodytext'] = text
