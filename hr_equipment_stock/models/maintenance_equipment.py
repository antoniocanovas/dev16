from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    quant_ids = fields.Many2many(
        comodel_name='stock.quant', store = True, readonly = True)

    @api.onchange('equipment_assign_to', 'department_id', 'employee_id')
    def get_quant_ids(self):
        for record in self:
            type = record.equipment_assign_to
            quants = []
            used_quants = []

            # Used quants:
            equipments = self.env['maintenance.equipment'].search([('active', '=', True)])
            for eq in equipments:
                for quant in eq.quant_ids: used_quants.append(quant.id)

            # CASE private quant of employee (employee in location):
            if (type == 'employee') and (record.employee_id.id):
                quants = self.env['stock.quant'].search(
                    [('employee_id', '=', record.employee_id.id), ('id', 'not in', used_quants)]).ids
            # CASE department material (department in location):
            elif (type == 'department') and (record.department_id.id):
                quants = self.env['stock.quant'].search(
                    [('department_id', '=', record.department_id.id), ('id', 'not in', used_quants)]).ids
            # CASE Material assigned to specific employee and department:
            elif (type == 'other') and (record.department_id.id) and (record.employee_id.id):
                quants = self.env['stock.quant'].search(
                    [('employee_id', '=', record.employee_id.id), ('department_id', '=', record.department_id.id),
                     ('id', 'not in', used_quants)]).ids
            # CASE Assigned to specific employee no department:
            elif (type == 'other') and not (record.department_id.id) and (record.employee_id.id):
                quants = self.env['stock.quant'].search(
                    [('employee_id', '=', record.employee_id.id), ('id', 'not in', used_quants)]).ids
            # CASE Assigned to specific department no employee:
            elif (type == 'other') and (record.department_id.id) and not (record.employee_id.id):
                quants = self.env['stock.quant'].search(
                    [('department_id', '=', record.department_id.id), ('id', 'not in', used_quants)]).ids
            record['available_quant_ids'] = [(6, 0, quants)]

    available_quant_ids = fields.Many2many('stock.quant', compute=get_quant_ids, store=False)

