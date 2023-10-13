from odoo import _, api, fields, models
from datetime import datetime, date

class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    contract_km = fields.Integer('Contracted km', store=True, copy=True)
    additional_km_cost = fields.Monetary('Additional km', store=True, copy=True)
    returned_km_cost = fields.Monetary('Returned km', store=True, copy=True)
    odometer = fields.Float('Last Odometer', store=True, copy=False, related='vehicle_id.odometer')

    @api.depends('expiration_date','start_date')
    def _get_leap_year_count(self):
        total, leaps = 0, [2000,2004,2008,2012,2016,2020,2024,2028,2032,2036,2040,2044,2048,2052,2056,2060,2064,2068]
        # Comprobación de si la fecha de inicio puede ser año bisiesto:
        if self.start_date.month > 2:
            start_year = self.start_date.year + 1
        else:
            start_year = self.start_date.year
        # Comprobación de si la fecha de expiración puede ser año bisiesto:
        if self.expiration_date.month > 2:
            expiration_year = self.expiration_date.year +1
        else:
            expiration_year = self.expiration_date.year
        # Número de años bisiestos en el contrato:
        for i in range(start_year, expiration_year):
            if i in leaps:
                total += 1
        self.year_leap_count = total
    year_leap_count = fields.Integer('Leap-year', store=True, copy=True, compute='_get_leap_year_count')

    @api.depends('contract_km','vehicle_id.odometer')
    def _get_pending_contract_km(self):
        self.pending_km = self.contract_km - self.vehicle_id.odometer
    pending_km = fields.Integer('Pending km', store=True, compute='_get_pending_contract_km')

    @api.depends('contract_km','expiration_date','start_date')
    def _get_annual_estimated_km(self):
        dif = self.expiration_date - self.start_date
        total_days = dif.days - self.year_leap_count
        self.annual_estimated_km = self.contract_km / ( total_days / 365 )
    annual_estimated_km = fields.Integer('Annual estimated km', store=True, copy=True, compute='_get_annual_estimated_km')

    @api.depends('start_date', 'vehicle_id.odometer', 'vehicle_id.odometer_ids.value')
    def _get_annual_consumed_km(self):
        annual_consumed_km, bisiestos = 0, [2024,2028,2032,2036,2040,2044,2048,2052,2056,2060]
        odometer_date = self.env['fleet.vehicle.odometer'].search([('vehicle_id', '=', self.vehicle_id.id)], order='date desc')[0]
        if odometer_date.id:
            dif = odometer_date.date - self.start_date
            total_days = dif.days - self.year_leap_count
            annual_consumed_km = self.vehicle_id.odometer / ( total_days / 365 )
        self.annual_consumed_km = annual_consumed_km
    annual_consumed_km = fields.Integer('Annual consumed km', store=True, compute='_get_annual_consumed_km')
