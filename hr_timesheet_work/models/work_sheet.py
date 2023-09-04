from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

TYPES = [
    ('project', 'Project'),
]

STATES = [
    ('new', 'New'),
    ('done', 'Done')
]


class TimeSheetWorkSheet(models.Model):
    _name = 'work.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Work Sheet'

    name = fields.Char('Name', required=True)
    date = fields.Date('Date', required=True)
    state = fields.Selection(selection=STATES, string="Status", default=STATES[0][0])
    work_id = fields.Many2one('timesheet.work')
    type = fields.Selection(string='Type', related='work_id.type')
    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task', string="Task")
    picking_ids = fields.One2many('stock.picking', 'work_sheet_id', string='Pickings')
    reinvoice_expense_ids = fields.One2many('hr.expense', 'work_sheet_id', string='Expenses',
                                            store=True, readonly=True,
                                            domain=[('sale_order_id','!=',False)]
                                            )
    line_done_ids = fields.One2many('timesheet.line.done', 'work_sheet_id', store=True)

    set_start_stop = fields.Boolean(related='work_id.set_start_stop', string='Set start & stop time')
    partner_id = fields.Many2one('res.partner', string='Signed by')
    signature = fields.Binary("Signature")
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')

    company_id = fields.Many2one(
        'res.company',
        'Company',
        store=False,
        default=lambda self: self.env.user.company_id
    )
    project_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Proj. Analytic',
        related='project_id.analytic_account_id'
    )
    project_so_id = fields.Many2one('sale.order', related='project_id.sale_order_id', store=True, string='Sale Order')

    project_service_ids = fields.One2many(
        'account.analytic.line',
        'work_sheet_id',
        domain=['|',('product_id','=',False),('product_id.type','=','service')],
        store=True,
        string='Imputaciones'
    )

    sheet_employee_ids = fields.One2many('work.sheet.employee', 'sheet_id', string='Employees', store=True)
    sheet_task_ids = fields.Many2many('work.sheet.task', string='Employees', store=True)

    # SO pickings available to add:
    @api.depends('work_id.sale_order_ids', 'picking_ids')
    def get_pending_order_pickings(self):
        for record in self:
            pickings = self.env['stock.picking'].search([('sale_id', 'in', record.work_id.sale_order_ids.ids),
                                                         ('state', 'not in', ['done', 'cancel']),
                                                         ('work_sheet_id', '=', False)])
            record['order_picking_ids'] = pickings.ids
    order_picking_ids = fields.Many2many('stock.picking', compute=get_pending_order_pickings, store=False)

    @api.depends('picking_ids')
    def get_project_products(self):
        for record in self:
            products = self.env['stock.move'].search([('picking_id','in',record.picking_ids.ids)])
            record.project_product_ids = [(6, 0, products.ids)]
    project_product_ids = fields.Many2many('stock.move', compute=get_project_products, store=False)


    task_sale_order_id = fields.Many2one('sale.order', related='task_id.sale_order_id', string='Sale Order')

    @api.depends('work_id')
    def get_projects(self):
        for record in self:
            projects = []
            partner = record.work_id.partner_id
            project = record.work_id.project_id
            if (partner.id) and (not project.id):
                projects = self.env['project.project'].search([('partner_id', '=', partner.id)]).ids
            elif (not partner.id) and (project.id):
                projects = self.env['project.project'].search([('id', '=', project.id)]).ids
            elif (partner.id) and (project.id):
                projects = self.env['project.project'].search([('id', '=', project.id)]).ids
            elif (not partner.id) and not (project.id):
                projects = self.env['project.project'].search([]).ids
            record.project_ids = [(6, 0, projects)]

    project_ids = fields.Many2many('project.project', compute=get_projects, store=False)

    #    @api.depends('project_service_ids', 'project_product_ids', 'repair_service_ids', 'repair_product_ids','mrp_service_ids', 'mrp_product_ids')
    @api.depends('project_service_ids', 'project_product_ids')
    def get_workread_only(self):
        for record in self:
            isreadonly = False
            #            if record.project_service_ids or record.project_product_ids or record.repair_service_ids.ids or record.repair_product_ids or record.mrp_service_ids or record.mrp_product_ids:
            if record.project_service_ids or record.project_product_ids:
                isreadonly = True
            record['work_readonly'] = isreadonly

    work_readonly = fields.Boolean(string='Read only', compute=get_workread_only, store=True)

    @api.depends('signature')
    def get_signed_report(self):
        for record in self:
            if record.signature and not record.signature_status:
                # generate pdf from report, use report's id as reference
                report_id = 'hr_timesheet_work.work_sheet_report'
                pdf = self.env.ref(report_id)._render_qweb_pdf(record.ids[0])
                # pdf result is a list
                b64_pdf = base64.b64encode(pdf[0])
                main_attachment = self.env['ir.attachment'].sudo().search(
                    ['&', ('res_id', '=', record.id), ('name', '=', str(record.time_type_id.name) + '.pdf')]
                )
                main_attachment.unlink()
                # save pdf as attachment
                name = record.name + (str(record.time_type_id.name))
                record.attachment_id = self.env['ir.attachment'].sudo().create({
                    'name': name + '.pdf',
                    'type': 'binary',
                    'datas': b64_pdf,
                    'store_fname': name + '.pdf',
                    'res_model': 'work.sheet',
                    'res_id': record.id,
                    'mimetype': 'application/pdf'
                })
                body = "<p>iSet Signed & Approved</p>"
                record.message_post(body=body, attachment_ids=[record.attachment_id.id])
                #self.message_main_attachment_id = [(4, self.attachment_id.id)]
                record.signature_status = True
            else:
                record.signature_status = False

    signature_status = fields.Boolean(string='Signed & Approved',  compute=get_signed_report, store=True)

    # ESTA ACCIÓN YA NO SE USA (31/10/2022), ahora está en el wizard:
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
            if (record.work_id.type == "project") and (record.project_id.id):
                for li in employee_ids:
                    if not li.user_id:
                        raise ValidationError('Empleado sin usuario asignado, revisa su ficha de empleado')
                    new = self.env['account.analytic.line'].create(
                        {'work_sheet_id': record.id, 'name': record.description, 'project_id': record.project_id.id,
                         'task_id': record.task_id.id, 'date': record.date, 'account_id': record.project_analytic_id.id,
                         'company_id': record.company_id.id, 'tag_ids': [(6,0,record.analytic_tag_ids.ids)],
                         'employee_id': li.id, 'unit_amount': duration, 'time_type_id': record.time_type_id.id,
                         'user_id':li.user_id.id
                         })
                    if (record.set_start_stop == True):
                        duration = record.stop - record.start
                        new.write({'time_start':record.start, 'time_stop':record.stop, 'unit_amount':duration})

            # CASE REPAIR:
            if (record.work_id.type == "repair") and (record.repair_id.id) and (record.project_id.id):
                for li in employee_ids:
                    if not li.user_id:
                        raise ValidationError('Empleado sin usuario asignado, revisa su ficha de empleado')
                    new = self.env['account.analytic.line'].create(
                        {'work_sheet_id': record.id, 'name': record.description, 'project_id': record.project_id.id,
                         'task_id': record.task_id.id, 'date': record.date, 'account_id': record.project_analytic_id.id,
                         'company_id': record.company_id.id, 'tag_ids': [(6,0,record.analytic_tag_ids.ids)],
                         'employee_id': li.id, 'unit_amount': duration, 'time_type_id': record.time_type_id.id,
                         'user_id':li.user_id.id, 'repair_id':record.repair_id.id
                         })
                    if (record.set_start_stop == True):
                        duration = record.stop - record.start
                        new.write({'time_start':record.start, 'time_stop':record.stop, 'unit_amount':duration})

    @api.depends('state')
    def update_employees_and_tasks_resume(self):
        for record in self:
            # Searching for unique employees and task names:
            unique_ts_task, name_unique_task, sheet_employee = [], [], []
            for aal in record.project_service_ids:
                if aal.employee_id not in sheet_employee: sheet_employee.append(aal.employee_id)

                name_task = str(aal.task_id.id) + aal.name
                if name_task not in name_unique_task:
                    unique_ts_task.append(aal)
                    name_unique_task.append(name_task)

            # Cleaning old data:
            for li in record.sheet_employee_ids:
                if li.employee_id.id not in sheet_employee: li.unlink()
            for li in record.sheet_task_ids:
                if li.task_id.id not in unique_ts_task: li.unlink()

            # Computing employees:
            for employee in sheet_employee:
                standard, extra, tasks = 0, 0, []
                exist = self.env['work.sheet.employee'].search(
                    [('sheet_id', '=', record.id), ('employee_id', '=', employee.id)])
                lines = self.env['account.analytic.line'].search(
                    [('work_sheet_id', '=', record.id), ('employee_id', '=', employee.id)])

                for li in lines:
                    if li.task_id.id not in tasks: tasks.append(li.task_id.id)

                    if (li.time_type_id.extra == True):
                        extra += li.unit_amount
                    else:
                        standard += li.unit_amount

                if not exist.id:
                    new = self.env['work.sheet.employee'].create({'employee_id': employee.id, 'sheet_id': record.id,
                                                                  'standard_time': standard, 'extra_time': extra,
                                                                  'task_ids':[(6,0,tasks)]})
                else:
                    exist.write({'employee_id': employee.id, 'sheet_id': record.id, 'task_ids':[(6,0,tasks)],
                                 'standard_time': standard, 'extra_time': extra})

            # Computing tasks: (voy revisando por aquí)
            task_list = []
            for aal in unique_ts_task:
                employees = []
                standard, extra, name = 0, 0, ""
                if aal.employee_id not in employees: employees.append(aal.employee_id.id)

                exist = self.env['work.sheet.task'].search([('sheet_id', '=', record.id), ('task_id', '=', aal.task_id.id)])
                lines = self.env['account.analytic.line'].search(
                    [('work_sheet_id', '=', record.id), ('task_id', '=', aal.task_id.id)])


                for li in lines:
                    if li.employee_id.id not in employees: employees.append(li.employee_id.id)
                    if (li.time_type_id.extra == True):
                        extra += li.unit_amount
                    else:
                        standard += li.unit_amount

                if not exist.id:
                    new = self.env['work.sheet.task'].create({'task_id': aal.task_id.id, 'sheet_id': record.id,
                                                              'name': aal.name, 'employee_ids':[(6,0,employees)],
                                                              'standard_time': standard, 'extra_time': extra})
                    task_list.append(new.id)
                else:
                    exist.write({'task_id': aal.task_id.id, 'sheet_id': record.id, 'name': aal.name,
                                 'employee_ids':[(6,0,employees)], 'standard_time': standard, 'extra_time': extra})
                    task_list.append(exist.id)
            record['sheet_task_ids'] = [(6, 0, task_list)]
