# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Comercialmente en cada pedido quieren saber cuántos pares se han vendido:
    def _get_shoes_pair_count(self):
        for record in self:
            count = 0
            for li in record.order_line:
                count += li.pairs_count
            record['pairs_count'] = count
    pairs_count = fields.Integer(string='Pairs', store=False, compute='_get_shoes_pair_count')

    shoes_campaign_id = fields.Many2one('project.project', string="Campaign", store=True, copy=True, tracking=10)

    def enable_sale_pairs(self):
        products = sef.env['product.template'].search([('shoes_campaign_id','=',self.shoes_campaign_id.id),('')])
        return True

    state_id = fields.Many2one("res.country.state", "Customer State", readonly=True, related='partner_id.state_id')

    def _get_campaign_top_sale(self):
        for record in self:
            models = []
            qty = self.env.company.top_sales_qty
            models = self.env['product.template'].search([
                ('shoes_campaign_id','=',record.shoes_campaign_id.id),('pairs_sold','>',1)], order='pairs_sold desc')
            record['campaign_top_ids'] = [(6,0,models.ids)]
    campaign_top_ids = fields.Many2many('product.template', store=False, compute='_get_campaign_top_sale')