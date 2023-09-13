from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    subscription_project_id = fields.Many2one('project.project', string='Task project',store=True, copy=True)
    create_task = fields.Selection(store=False, related='template_id.create_task')