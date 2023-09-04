# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _


class WorkPickingWizard(models.TransientModel):
    _name = "work.picking.wizard"
    _description = "Work Sheet Picking Wizard"

    work_sheet_id = fields.Many2one('work.sheet', string='Sheet', store=True)
    picking_ids = fields.Many2many('stock.picking', related='work_sheet_id.order_picking_ids')
    picking_selection_ids = fields.Many2many('stock.picking', string="Selecteds")

    def assign_work_sheet(self):
        for sp in self.picking_selection_ids:
            sp['work_sheet_id'] = self.work_sheet_id.id
