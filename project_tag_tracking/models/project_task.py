# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

#    tag_ids = fields.Many2many(tracking=100)
    tag_tracking = fields.Text('Tags tracking', store=True, tracking=100)
    tag_prev_ids = fields.Many2one(store=True, copy=False, string="Previous tags",
        comodel_name="project.tags",
        relation='task_tags_rel',
        column1='task_id',
        column2='tag_id',
    )


    def update_task_tracking(self):
        newtags, deletedtags, tagtracking = [], [], ""
        for tag in self.tag_ids.ids:
            if tag not in self.tag_prev_ids.ids:
                newtags.append(tag)
                tag = env['project.tags'].search([('id', '=', tag)])
                tagtracking += "(+) " + tag.name + "\n"
        for tag in self.tag_prev_ids.ids:
            if tag not in self.tag_ids.ids:
                deletedtags.append(tag)
                tag = env['project.tags'].search([('id', '=', tag)])
                tagtracking += "(-) " + tag.name + "\n"
        if tagtracking != "":
            self.write({'tag_prev_ids': [(6, 0, newtags)], 'description': tagtracking})
