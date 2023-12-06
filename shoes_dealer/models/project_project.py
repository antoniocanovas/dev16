# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    # Cambio de moneda estimado para cálculo de precios de pares y surtidos en base a exwork:
    currency_exchange = fields.Float('Dollar exchange', store=True, copy=False)
