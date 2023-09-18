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
            if not (record.user_id.id) and (record.team_id.id == record.website_id.salesteam_id.id):
                rental = False
                for li in record.order_line:
                    if li.product_template_id.rent_ok: rental = True
                if (rental == False):
                    raise UserError('Nada que alquilar')
                else:
                    if not (record.commitment_date):
                        raise UserError("Pon fecha de entrega")
                    else:
                        record['is_rental_order'] = True
                        for li in record.order_line:
                            rentalday = record.rental_date
                            reservation_begin = datetime(rentalday.year, rentalday.month, rentalday.day, 0,0,0)
                            reservation_end = datetime(rentalday.year, rentalday.month, rentalday.day, 23,0, 0)
                            li.write({'is_rental': True, 'start_date': reservation_begin, 'return_date': reservation_end})