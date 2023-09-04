# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WorkTimesheetWizard(models.TransientModel):
    _name = "work.timesheet.wizard"
    _description = "Work Sheet Timesheet Wizard"


    name = fields.Char('Name', store=True, readonly=False)
    work_sheet_id = fields.Many2one('work.sheet', string='Sheet', store=True)
    date = fields.Date('Date')
    project_id = fields.Many2one('project.project', string='Project', store=True)
    task_id = fields.Many2one('project.task', string='Task', store=True)
    time_type_id = fields.Many2one('project.time.type', string='Schedule')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    start = fields.Float('Start')
    stop = fields.Float('Stop')
    duration = fields.Float('Duration', store=True)
    version = fields.Integer('Version', default=0)
    set_start_stop = fields.Boolean(related='work_sheet_id.work_id.set_start_stop', string='Set start & stop time')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', store=True, string='Tags',
                                        domain=[('timesheet_hidden', '=', False)]
                                        )


    work_id = fields.Many2one('timesheet.work', string='Work', related='work_sheet_id.work_id')
    todo_id = fields.Many2one('timesheet.line.todo', string='Milestone', store=True)
    todo_uom_id = fields.Many2one('uom.uom', string='UOM', related='todo_id.uom_id')
    todo_qty = fields.Float('Qty')

    @api.depends('version')
    def get_line_done_ids(self):
        self.done_ids = [(6,0,self.work_sheet_id.line_done_ids.ids)]
    done_ids = fields.Many2many('timesheet.line.done', store=True, readonly=False,
                                compute="get_line_done_ids")



    @api.depends('version')
    def get_work_sheet_timesheets(self):
        self.timesheet_ids = [(6,0,self.work_sheet_id.project_service_ids.ids)]
    timesheet_ids = fields.Many2many('account.analytic.line', store=True, readonly=False,
                                     compute="get_work_sheet_timesheets")

    def create_lot_worksheet_services(self):
        # Check required fields:
        for record in self:
            # Required start to concatenate later, required duration to change later if startstop:
            start = ""
            duration = record.duration

            # Chek task assigned:
            if (record.task_id.id == False):
                raise ValidationError('Please, assign the task you have been working.')

            # Chek time consumed:
            if (record.set_start_stop == False) and (record.duration == 0):
                raise ValidationError('Please, set the time consumed in Duration.')
            elif (record.set_start_stop == True) and ((record.stop - record.start) <= 0):
                raise ValidationError('Please review start & stop time consumed.')

            # CASE USER NOT ADMINISTRATOR, CAN'T SEE FIELD employee_ids => Self timesheet:
            if record.employee_ids.ids:
                employee_ids = record.employee_ids
            else:
                employee_ids = [self.env.user.employee_id]

            # CASE PROJECT:
            if (record.work_sheet_id.work_id.type == "project") and (record.project_id.id):
                for li in employee_ids:
                    if not li.user_id:
                        raise ValidationError('Empleado sin usuario asignado, revisa su ficha de empleado')
                    new = self.env['account.analytic.line'].create(
                        {'work_sheet_id': record.work_sheet_id.id, 'name': record.name,
                         'project_id': record.project_id.id,
                         'task_id': record.task_id.id, 'date': record.date,
                         'account_id': record.work_sheet_id.project_analytic_id.id,
                         'company_id': record.work_sheet_id.company_id.id,
                         'tag_ids': [(6,0,record.analytic_tag_ids.ids)],
                         'employee_id': li.id, 'unit_amount': duration, 'time_type_id': record.time_type_id.id,
                         'user_id':li.user_id.id,
                         'wizard_id': record.id
                         })
                    if (record.set_start_stop == True):
                        duration = record.stop - record.start
                        new.write({'time_start':record.start, 'time_stop':record.stop, 'unit_amount':duration})
                    record['version'] = record.version + 1

        return {
            'name': 'Work Sheet Add Timesheet wizard view',
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'work.timesheet.wizard',
            'type': 'ir.actions.act_window',
            'view_id':
                self.env.ref('hr_timesheet_work.work_timesheet_wizard_default_form').id,
            'context': dict(self.env.context),
            'target': 'new',
            'res_id': self.id,
        }

    def create_milestones(self):
        for record in self:
            duration = record.duration * len(record.employee_ids.ids)
            if (record.todo_id.id) and (record.todo_qty != 0):
                new_done = self.env['timesheet.line.done'].create({'work_sheet_id':record.work_sheet_id.id,
                                                                   'todo_id': record.todo_id.id, 'name': record.name,
                                                                   'time_elapsed': duration, 'qty':record.todo_qty
                                                                   })
            record['version'] = record.version + 1
        return {
            'name': 'Work Sheet Add Timesheet wizard view',
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'work.timesheet.wizard',
            'type': 'ir.actions.act_window',
            'view_id':
                self.env.ref('hr_timesheet_work.work_timesheet_wizard_default_form').id,
            'context': dict(self.env.context),
            'target': 'new',
            'res_id': self.id,
        }


