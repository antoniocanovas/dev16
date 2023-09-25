# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    website_sale_id = fields.Many2one('sale.order', string='Website Sale', store=True, copy=False)

    def website_sale_purchase_auto_confirm(self):
        for record in self:
            confirm, website_sale_id = False, False
            for li in record.order_line:
                if (li.sale_line_id.id) and (li.sale_order_id.team_id.id == 2):
                    website_sale_id = li.sale_order_id
                    confirm = True
            if (confirm == True):
                record.write({'website_sale_id':website_sale_id.id})
                record.button_confirm()