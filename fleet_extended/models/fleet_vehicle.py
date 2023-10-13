from odoo import _, api, fields, models
from datetime import datetime, date

class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle'

    odometer_ids = fields.One2many('fleet.vehicle.odometer', 'vehicle_id' store=True, copy=False)
