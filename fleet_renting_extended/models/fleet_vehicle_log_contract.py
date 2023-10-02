from odoo import _, api, fields, models
from datetime import datetime, date

class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    contract_km = fields.Integer('Contracted km', store=True, copy=True)
    additional_km_cost = fields.Monetary('Additional km', store=True, copy=True)
    returned_km_cost = fields.Monetary('Returned km', store=True, copy=True)

    def _get_pending_contract_km(self):
        self.pending_km = self.contract_km - self.vehicle_id.odometer
    pending_km = fields.Integer('Pending km', store=False, compute='_get_pending_contract_km')

    def _get_annual_estimated_km(self):
        dif = self.expiration_date - self.start_date
        self.annual_estimated_km = self.contract_km / ( dif.days / 365 )
    annual_estimated_km = fields.Integer('Annual estimated km', store=False, copy=True, compute='_get_annual_estimated_km')

    def _get_annual_consumed_km(self):
        dif = date.today() - self.start_date
        self.annual_consumed_km = self.vehicle_id.odometer - ( dif.days / 365 )
    annual_consumed_km = fields.Integer('Annual consumed km', store=False, compute='_get_annual_consumed_km')
