# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    customer_id = fields.Many2one('res.partner', string='Customer', related='sale_order_id.partner_id')
    sale_commitment_date = fields.Datetime('Commitment date', related='sale_line_id.commitment_date', store=True)

    @api.depends('create_date')
    def _get_sale_event(self):
        for record in self:
            if not record.event_id.id:
                record.event_id = record.sale_order_id.event_id.id
    event_id = fields.Many2one('event.event', string='Event', readonly=False, store=True,
                               domain=[('stage_id.pipe_end','=',False),('is_published','=',True)],
                               compute='_get_sale_event'
                               )

    @api.depends('create_date')
    def _get_sale_stand_name(self):
        for record in self:
            record.stand_name = record.sale_order_id.stand_name
    stand_name = fields.Char('Stand name', store=True, readonly=False, compute='_get_sale_stand_name')

    @api.depends('create_date')
    def _get_sale_stand_number(self):
        for record in self:
            record.stand_number = record.sale_order_id.stand_number
    stand_number = fields.Char('Stand number', store=True, readonly=False, compute='_get_sale_stand_number' )