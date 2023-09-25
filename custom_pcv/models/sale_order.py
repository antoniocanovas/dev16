# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

MONTHS = [('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),
          ('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12')]


class SaleOrder(models.Model):
    _inherit = "sale.order"


    cc_name = fields.Char('Card name')
    cc_number = fields.Char('Card number')
    cc_expire_month = fields.Selection(selection=MONTHS, string="Card Month expiration", store=True)
    cc_expire_year  = fields.Integer('Year expiration', store=True)
    event_id        = fields.Many2one('event.event', string='Event',
                                      domain=[('stage_id.pipe_end','=',False),('is_published','=',True)])
    stand_name      = fields.Char('Stand name', store=True)
    stand_number    = fields.Char('Stand number', store=True)
