# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    #   Versión antigua: tag_ids = fields.Many2many(tracking=100)
    tag_prev_ids = fields.Many2many(store=True, copy=False, string="Previous tags", readonly="1",
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
                tagtracking += "<p>(+) " + tag.name + "</p>"
        for tag in self.tag_prev_ids.ids:
            if tag not in self.tag_ids.ids:
                tag = self.env['project.tags'].search([('id', '=', tag)])
                tagtracking += "<p>(-) " + tag.name + "</p>"
        if tagtracking != "":
            self.write({'tag_prev_ids': [(6, 0, self.tag_ids.ids)], 'description': tagtracking})
            new_note = self.env['mail.message'].create({'body': tagtracking,
                                                        'message_type': 'comment',
                                                        'model': 'project.task',
                                                        'res_id': self.id,
                                                        })
            
