from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TYPE = [
    ('sale', 'Sale'),
    ('project', 'Project'),
    ('task', 'Tasks'),
    ('warranty', 'Maintenance or warranty'),
]

class ExternalWork(models.Model):
    _name = "external.work"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "External Work"

    type = fields.Selection(selection=TYPE, string="Type", default=TYPE[0][0])

    subject     = fields.Char('Subject')
    date        = fields.Date('Date')

    employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user.employee_id)
    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    project_id  = fields.Many2one('project.project', string="Project")
    task_id     = fields.Many2one('project.task', string="Task")
    sale_id     = fields.Many2one('sale.order', string="Sale")
    sale_state  = fields.Selection(related='sale_id.state')
    partner_id  = fields.Many2one('res.partner', string="Partner")
    sale_subtotal = fields.Monetary('Sale subtotal', related='sale_id.amount_untaxed')
    signed_by   = fields.Char('Signed by')
    signature   = fields.Binary('Signature')
    line_ids    = fields.One2many('external.work.line', 'external_work_id', string='Lines')
    company_id  = fields.Many2one('res.company')
    currency_id = fields.Many2one('res.currency', store=True, default=1)
    state       = fields.Selection([('draft','Draft'),('done','Done')], store=True, default='draft')
    expense_ids = fields.One2many('hr.expense', 'external_work_id', string='Expenses')

    @api.depends('create_date')
    def _get_external_work_code(self):
        self.code = self.env['ir.sequence'].next_by_code('external.work.sequence')
    code = fields.Char('Code', store=True, readonly=True, compute=_get_external_work_code)

    @api.depends('sale_id')
    def _get_default_note_from_sale_id(self):
        for record in self:
            note = ""
            if (record.sale_id.id) and (record.note == "") and (record.sale_id.note != ""):
                note = record.sale_id.note
            record['note'] = note
    note = fields.Text('Note', store=True, compute=_get_default_note_from_sale_id, readonly=False)

    @api.depends('line_ids')
    def get_line_count(self):
        self.line_count = len(self.line_ids.ids)
    line_count  = fields.Integer('Lines', store=False, compute='get_line_count')

    @api.depends('line_ids')
    def get_expense_count(self):
        self.expense_count = len(self.expense_ids.ids)
    expense_count  = fields.Integer('Expense count', store=False, compute='get_expense_count')

    @api.depends('code', 'subject')
    def _get_work_name(self):
        name=""
        if self.code: name += "[" + self.code + "] "
        if self.subject: name += self.subject
        self.name = name
    name = fields.Char('Name', compute='_get_work_name', store=True)

    def action_work_update(self):
        # Create or update sale.order if not:
        if not self.sale_id.id:
            create_sale = False
            for li in self.line_ids:
                if li.type in ['ein', 'sin', 'pin', 'pno']: create_sale = True
            if create_sale == True:
                sale = self.env['sale.order'].create({'partner_id':self.partner_id.id, 'note':self.note})
                self.sale_id = sale.id
        else:
            self.sale_id['note'] = self.note

        # Models to check:
        for li in self.line_ids:
            timesheet, saleline, expense, newsol = False, False, False, False
            if (li.type in ['ein','pin','pni','sin']) and (li.is_readonly == False): saleline = True
            if (li.type in ['sin','sni']) and (li.is_readonly == False): timesheet = True
            if (li.type in ['ein','eni']) and (li.is_readonly == False): expense = True

            # EMPLOYEE EXPENSES (if not, sale line will not be created):
            if (expense == True) and (li.hr_expense_id.id == False):
                newexpense = self.env['hr.expense'].create({'employee_id':li.employee_id.id, 'name': li.name,
                                                            'date': li.date, 'payment_mode':'own_account',
                                                            'unit_amount':li.ticket_amount / li.product_qty,
                                                            'product_id':li.product_id.id, 'quantity':li.product_qty,
                                                            'product_uom_id':li.uom_id.id,
                                                            'external_work_id':self.id
                                                            })
                li.hr_expense_id = newexpense.id
            elif (expense == True) and (li.hr_expense_id.id != False):
                amount = 0
                if li.product_qty != 0: amount = li.ticket_amount / li.product_qty
                li.hr_expense_id.write({'employee_id':li.employee_id.id, 'name': li.name,
                                        'date': li.date, 'payment_mode':'own_account',
                                        'product_id':li.product_id.id, 'quantity':li.product_qty,
                                        'unit_amount':amount, 'product_uom_id':li.uom_id.id,
                                        'external_work_id':self.id
                                        })

            # SALE LINE FOR PRODUCT OR SERVICE:
            name = "[" + self.code + "] " + li.product_id.name
            # Sale order based on list price:
            if (saleline == True) and (li.sale_line_id.id == False) and (li.type in ['pin','sin','ein']):
                newsol = self.env['sale.order.line'].create({'product_id':li.product_id.id, 'name':name,
                                                             'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                                             'order_id':self.sale_id.id})
                # Line with price = 0:
            elif (saleline == True) and (li.sale_line_id.id == False) and (li.type in ['pni']):
                newsol = self.env['sale.order.line'].create({'product_id':li.product_id.id, 'name':name,
                                                             'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                                             'order_id':self.sale_id.id, 'price_unit':0})
                # Overwrite line with list price:
            elif (saleline == True) and (li.sale_line_id.id == False) and (li.type in ['pin','sin','ein']):
                li.sale_line_id.write({'product_id':li.product_id.id, 'name':name,
                                       'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                       'order_id':self.sale_id.id})
                # Overwrite line with price = 0
            elif (saleline == True) and (li.sale_line_id.id != False) and (li.type in ['pni']):
                li.sale_line_id.write({'product_id':li.product_id.id, 'name':name,
                                       'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                       'order_id':self.sale_id.id, 'price_unit':0})
            if newsol: li.sale_line_id = newsol.id

            # EMPLOYEE TIMESHEETS:
            if (timesheet == True) and (li.analytic_line_id.id == False):
                newts = self.env['account.analytic.line'].create({'name':li.name, 'date':li.date,
                                                                  'task_id':li.task_id.id,
                                                                  'account_id':li.project_id.analytic_account_id.id,
                                                                  'amount':li.product_qty * li.product_id.standard_price,
                                                                  'unit_amount':li.product_qty, 'product_id':li.product_id.id,
                                                                  'employee_id':li.employee_id.id})
                li.analytic_line_id = newts.id
            elif (timesheet == True) and (li.analytic_line_id.id != False):
                li.analytic_line_id.write({'name':li.name, 'date':li.date,
                                           'task_id':li.task_id.id,
                                           'account_id':li.project_id.analytic_account_id.id,
                                           'amount':li.product_qty * li.product_id.standard_price,
                                           'unit_amount':li.product_qty, 'product_id':li.product_id.id,
                                           'employee_id':li.employee_id.id})

    def action_work_confirm(self):
        self.action_work_update()
        self.state = 'done'

    def action_work_back2draft(self):
        # Check if possible, deleting timesheet, expense and salelines:
        if self.sale_state != 'draft':
            raise ValidationError("Sale order state must be DRAFT to back this Work")
        self.write({'state':'draft', 'signature':False})

