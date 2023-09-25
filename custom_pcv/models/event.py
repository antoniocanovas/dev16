# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ProductBrand(models.Model):
    _inherit = "event.event"


    assembly = fields.Html(string='Assembly', store=True, translate=True)
    disassembly = fields.Html(string='Disassembly', store=True, translate=True)
