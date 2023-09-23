# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

#    tag_ids = fields.Many2many(tracking=100)
    tag_tracking = fields.Text('Tags tracking', store=True, tracking=100)
    tag_prev_ids = fields.Many2Many(store=True, copy=False, string="Previous tags",
        comodel_name="project.tags",
        relation='task_tags_rel',
        column1='task_id',
        column2='tag_id',
    )


    def update_task_tracking(self):
        tagtracking = ""
        for tag in self.tag_ids.ids:
            if tag not in self.tag_prev_ids.ids:
                tag = self.env['project.tags'].search([('id', '=', tag)])
                tagtracking += "(+) " + tag.name + "\n"
        for tag in self.tag_prev_ids.ids:
            if tag not in self.tag_ids.ids:
                tag = self.env['project.tags'].search([('id', '=', tag)])
                tagtracking += "(-) " + tag.name + "\n"
        if tagtracking != "":
            tags = [(6, 0, self.tag_ids.ids)]
            self.write({'tag_prev_ids': tags, 'description': tagtracking})
