from odoo import _, api, fields, models
from datetime import date

TYPE = [
    ('pin', 'Product billable'),
    ('pni', 'Product not billable'),
    ('sin', 'Technical Service billable'),
    ('sni', 'Technical Service not billable'),
    ('ein', 'Employee expense billable'),
    ('eni', 'Internal employee expense'),
]

class ExternalWork(models.Model):
    _name = "external.work.line"
    _description = "External Work Line"


    @api.depends('external_work_id','employee_id')
    def _get_workline_name(self):
        for record in self:
            name=""
            if record.external_work_id.id: name += str(record.external_work_id.name)
            if name: name += " - "
            if record.product_id.id: name += str(record.product_id.name)
            record['name'] = name
    name = fields.Char('Name', compute='_get_workline_name')

    type        = fields.Selection(selection=TYPE, string="Type", default=TYPE[0][0])
    date        = fields.Date(string='Date', readonly=False, default=date.today())

    @api.depends('external_work_id')
    def _get_default_employee(self):
        self.employee_id = self.external_work_id.employee_id.id
    employee_id = fields.Many2one('hr.employee', string="Employee", store=True,
                                  readonly=False, compute=_get_default_employee)

    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    partner_id  = fields.Many2one('res.partner', string="Partner", related='external_work_id.partner_id')
    material_id = fields.Many2one('product.product', string='Material', domain="[('sale_ok','=',True)]")
    service_id  = fields.Many2one('product.product', string='Work product', domain="[('is_work_time','=',True),('sale_ok','=',True)]")
    expense_id  = fields.Many2one('product.product', string='Expense', domain="[('can_be_expensed','=',True)]")

    @api.depends('type','material_id','service_id','expense_id')
    def _get_product_id(self):
        for record in self:
            product = record.material_id
            if record.type in ['ein','eni']: product = record.expense_id
            if record.type in ['sin','sni']: product = record.service_id
            record['product_id'] = product.id
    product_id  = fields.Many2one('product.product', string='Product', compute='_get_product_id', store=True)
    uom_id      = fields.Many2one('uom.uom', string='UOM', related='product_id.uom_id')

    @api.depends('time_begin','time_end')
    def _get_time_elapsed(self):
        for record in self:
            qty = record.product_qty
            if (record.type in ['sin','sni']) and (record.time_begin < record.time_end) and ((record.time_begin - record.time_end) != 0):
                qty = record.time_end - record.time_begin
            record['time_elapsed'] = qty
    time_elapsed = fields.Float('Time elapsed', store=True, compute=_get_time_elapsed)

    @api.depends('time_elapsed')
    def _get_timesheet_qty(self):
        for record in self:
            if record.time_elapsed != 0:
                record['product_qty'] = record.time_elapsed
    product_qty = fields.Float('Qty', store=True, readonly=False, compute=_get_timesheet_qty, default="1")

    ticket_amount = fields.Monetary('Ticket value', store=True, readonly=False)
    currency_id = fields.Many2one('res.currency', store=True, default=1)

    @api.depends('external_work_id')
    def _get_default_project_id(self):
        self.project_id = self.external_work_id.project_id.id
    project_id  = fields.Many2one('project.project', string="Project", store=True,
                                  readonly=False, compute=_get_default_project_id)

    @api.depends('external_work_id')
    def _get_default_task_id(self):
        self.task_id = self.external_work_id.task_id.id
    task_id     = fields.Many2one('project.task', string="Task", store=True,
                                  readonly=False, compute=_get_default_task_id)

    time_begin  = fields.Float('Begin')
    time_end    = fields.Float('End')

    hr_expense_id       = fields.Many2one('hr.expense', 'Expense line')
    hr_expense_state    = fields.Selection(related='hr_expense_id.state')
    analytic_line_id    = fields.Many2one('account.analytic.line')
    sale_line_id        = fields.Many2one('sale.order.line')
    sale_id             = fields.Many2one('sale.order', string="Sale", related='external_work_id.sale_id')
    sale_state          = fields.Selection(related='sale_id.state')
    external_work_id    = fields.Many2one('external.work', string='Work')
    work_type           = fields.Selection('Work type', related='external_work_id.type')

    # IDS lines so for record in self is required:
    @api.depends('sale_state','hr_expense_state','external_work_id.state')
    def _get_workline_is_readonly(self):
        for record in self:
            is_readonly = False
            if (record.hr_expense_id.id) and (record.hr_expense_state != 'draft') and (record.type in ['ein','eni']): is_readonly = True
            if (record.sale_state != 'draft') and (record.type in ['ein','pin','pni','sin']) and (record.id) and (record.sale_line_id): is_readonly = True
            record['is_readonly'] = is_readonly
    is_readonly = fields.Boolean('Is readonly', compute='_get_workline_is_readonly', store=True, readonly=True)


