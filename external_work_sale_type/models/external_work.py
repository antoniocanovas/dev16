from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ExternalWork(models.Model):
    _inherit = 'external.work'

    @api.depends('sale_id')
    def _get_sale_order_type(self):
        for record in self:
            type = False
            if record.sale_id.id:
                type = record.sale_id.type_id.id
            record['sale_type_id'] = type
    sale_type_id = fields.Many2one('sale.order.type', string="Sale type", store=True, required=True,
                                   readonly=False, compute='_get_sale_order_type')

    def action_work_update(self):
        # Create or update sale.order if not:
        if not self.sale_id.id:
            create_sale = False
            for li in self.line_ids:
                if li.type in ['ein', 'sin', 'pin', 'pno']: create_sale = True
            if create_sale == True:
                sale = self.env['sale.order'].create({'partner_id':self.partner_id.id, 'note':self.note, 'type_id':self.sale_type_id.id})
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
            # Sale order based on list price:
            if (saleline == True) and (li.sale_line_id.id == False) and (li.type in ['pin','sin','ein']):
                newsol = self.env['sale.order.line'].create({'product_id':li.product_id.id, 'name':li.product_id.name,
                                                             'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                                             'order_id':self.sale_id.id})
                # Line with price = 0:
            elif (saleline == True) and (li.sale_line_id.id == False) and (li.type in ['pni']):
                newsol = self.env['sale.order.line'].create({'product_id':li.product_id.id, 'name':li.product_id.name,
                                                             'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                                             'order_id':self.sale_id.id, 'price_unit':0})
                # Overwrite line with list price:
            elif (saleline == True) and (li.sale_line_id.id == False) and (li.type in ['pin','sin','ein']):
                li.sale_line_id.write({'product_id':li.product_id.id, 'name':li.product_id.name,
                                       'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                       'order_id':self.sale_id.id})
                # Overwrite line with price = 0
            elif (saleline == True) and (li.sale_line_id.id != False) and (li.type in ['pni']):
                li.sale_line_id.write({'product_id':li.product_id.id, 'name':li.product_id.name,
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

