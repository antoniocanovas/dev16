from odoo import _, api, fields, models
from datetime import datetime, date

class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    contract_km = fields.Integer('Contracted km', store=True, copy=True)
    additional_km_cost = fields.Monetary('Additional km', store=True, copy=True)
    returned_km_cost = fields.Monetary('Returned km', store=True, copy=True)

    @api.depends('contract_km','vehicle_id.odometer')
    def _get_pending_contract_km(self):
        self.pending_km = self.contract_km - self.vehicle_id.odometer
    pending_km = fields.Integer('Pending km', store=True, compute='_get_pending_contract_km')

    @api.depends('contract_km','expiration_date','start_date')
    def _get_annual_estimated_km(self):
        dif = self.expiration_date - self.start_date
        self.annual_estimated_km = self.contract_km / ( dif.days / 365 )
    annual_estimated_km = fields.Integer('Annual estimated km', store=True, copy=True, compute='_get_annual_estimated_km')

    @api.depends('start_date', 'vehicle_id.odometer')
    def _get_annual_consumed_km(self):
        annual_consumed_km = 0
        odometer_date = self.env['fleet.vehicle.odometer'].search([('vehicle_id', '=', self.vehicle_id.id)], order='date desc')[0]
        if odometer_date.id:
            dif = odometer_date.date - self.start_date
            annual_consumed_km = self.vehicle_id.odometer / ( dif.days / 365 )
        self.annual_consumed_km = annual_consumed_km
    annual_consumed_km = fields.Integer('Annual consumed km', store=True, compute='_get_annual_consumed_km')
