# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    # Para borrar después de la migración:
    currency_exchange = fields.Float('Dollar exchange', store=True, copy=False)
