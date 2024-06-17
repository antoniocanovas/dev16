# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError

def _prepare_data(env, data):
    if data.get('active_model') == 'stock.picking':
        picking = env['stock.picking']
    else:
        raise UserError(_('Model not defined, Please contact your administrator.'))

    picking_ids = data.get('picking_ids')
    pickings = picking.search([('id', 'in', picking_ids)], order='name desc')
    layout_wizard = env['stock.picking.report.wizard'].browse(data.get('layout_wizard'))

    if not layout_wizard:
        return {}

    return {
        'pickings': pickings,
        'parcels': layout_wizard.pnt_parcels,
    }

class ReportProductTemplateLabel(models.AbstractModel):
    _name = 'report.custom_azarey.pnt_report_stocktemplatelabel'
    _description = 'PNT stock Label Report'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)
