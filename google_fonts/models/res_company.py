# Copyright 2020 Ecosoft Co., Ltd (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    font = fields.Selection(
        selection_add=[
            ("OpenSans", "OpenSans"),
            ("OpenSans_italic", "OpenSans_italic"),
            ("Poly", "Poly"),
            ("Poly_italic", "Poly_italic"),
        ]
    )
