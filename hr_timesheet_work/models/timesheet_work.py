from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


TYPES = [
    ('project', 'Project'),
]


class TimesheetWork(models.Model):
    _name = 'timesheet.work'
    _description = 'Timesheet Work'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    type = fields.Selection([('project','Project')],
                            required=True, string='Type', default='project', index=True, copy=False, tracking=True)
    project_id = fields.Many2one('project.project')
    set_start_stop = fields.Boolean('Set start & stop time')
    sale_order_ids = fields.Many2many('sale.order', string='Sale Orders')
    todo_ids = fields.One2many('timesheet.line.todo', 'work_id')
    done_ids = fields.One2many('timesheet.line.done', 'work_id')

    @api.depends('todo_ids')
    def get_todo_count(self):
        for record in self:
            record.todo_count = len(record.todo_ids.ids)
    todo_count = fields.Integer(string='To-do', store=False, compute='get_todo_count',)

    @api.depends('done_ids')
    def get_done_count(self):
        for record in self:
            record.done_count = len(record.done_ids.ids)
    done_count = fields.Integer(string='Done', store=False, compute='get_done_count',)


    # Action in buttom box to import sale order lines to lines to-do:
    def import_sale_line_todo(self):
        lines = self.env['sale.order.line'].search([('display_type', '=', False), ('order_id', 'in', self.sale_order_ids.ids)])
        for li in lines:
            exist = self.env['timesheet.line.todo'].search([('sale_line_id', '=', li.id)])
            if not exist.ids:
                self.env['timesheet.line.todo'].create({'work_id': self.id, 'sale_line_id': li.id, 'name': li.name,
                                                        'product_id': li.product_id.id, 'uom_id': li.product_uom.id})
    # - - - - - -