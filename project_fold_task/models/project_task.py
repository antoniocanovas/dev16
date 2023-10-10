# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    #   Utilizado para filtrar las tareas con usuarios asignados, que pertenecen a las plantillas:
    project_fold = fields.Boolean(store=True, copy=False, string="Project fold", related='project_id.fold')
