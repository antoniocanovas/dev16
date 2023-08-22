# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    analytic_line_ids = fields.One2many('account.analytic.line', 'svl_id', string='Analytic Lines', store="True",)

    @api.depends('create_date')
    def analytic_picking_auto(self):
        for record in self:
            move = record.stock_move_id
            picking = move.picking_id
            plan = move.analytic_distribution
            status = picking.state
            code = picking.picking_type_id.code

            exist = record.analytic_line_ids
            name = record.description
            quantity = record.quantity
            uom = record.uom_id
            value = record.value

            if (move.id and picking.id and plan and not exist.ids and status == 'done') and (code in ['incoming','outgoing']):
              for aa,percent in plan.items():
                analytic = self.env['account.analytic.account'].search([('id','=',int(aa))])
                new = self.env['account.analytic.line'].create({'name':name,
                                                                'account_id':analytic.id,
                                                                'product_id':record.product_id.id,
                                                                'product_uom_id':uom.id,
                                                                'unit_amount':quantity,
                                                                'amount':value * percent / 100,
                                                                'svl_id': record.id
                                                                })
