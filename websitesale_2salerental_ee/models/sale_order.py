# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"

    rental_date = fields.Date('Rental date', store=True)

    @api.depends('rental_date')
    def sale_to_rent(self):
        for record in self:
            rental = False
            for li in record.order_line:
                if li.product_template_id.rent_ok: rental = True
            if (rental == False) and (record.user_id.id):
                raise UserError('Nada que alquilar')
            else:
                if not (record.rental_date) and (record.user_id.id):
                    raise UserError("Pon fecha de servicio")
                else:
                    if (record.is_rental_order == False):
                        record.write({'is_rental_order': True, 'rental_status':'draft'})
                    for li in record.order_line:
                        rentalday = record.rental_date
                        reservation_begin = datetime(rentalday.year, rentalday.month, rentalday.day, 4,0,0)
                        reservation_end = datetime(rentalday.year, rentalday.month, rentalday.day, 21,0, 0)
                        li.write({'is_rental': True, 'start_date': reservation_begin, 'return_date': reservation_end})