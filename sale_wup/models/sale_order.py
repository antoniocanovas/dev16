from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrderWup(models.Model):
    _inherit = 'sale.order'

    wup_line_ids = fields.One2many('wup.line','sale_id', string='wup')
    #Avoid same project when duplicating sale order:
    project_id = fields.Many2one('project.project', copy=False)

    def _get_wup_line_count(self):
        for record in self:
            total = 0
            results = self.env['wup.line'].search([('sale_id', '=', record.id)])
            if results: total = len(results)
            record.wup_line_count = total
    wup_line_count = fields.Integer('wups', compute=_get_wup_line_count)

    def get_worksheets_products(self):
        for record in self:
            extra = []
            if record.analytic_account_id.id:
                aal_ids = self.env['account.analytic.line'].search([
                    ('account_id','=',record.analytic_account_id.id),
                    ('product_id.type','in',['product','consu'])])
                for aal in aal_ids:
                    svl = self.env['stock.valuation.layer'].search([('analytic_id', '=', aal.id)])
                    sm = svl.stock_move_id
                    if (svl.id) and not (sm.sale_line_id.id):
                        extra.append(aal.id)
            record.product_consumed_ids = [(6, 0, extra)]
    product_consumed_ids = fields.Many2many('account.analytic.line', compute=get_worksheets_products, store=False)
    new_sale_id = fields.Many2one('sale.order', string='New quotation')

    def action_view_wup_line(self):
        action = self.env.ref(
            'sale_wup.action_view_wups').read()[0]
        return action

