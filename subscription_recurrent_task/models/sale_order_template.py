from odoo import _, api, fields, models


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    create_task = fields.Selection([('draft','Draft invoice'),('confirm','Confirmed invoice')], store=True, copy=True,
                                   string='Task creation')
