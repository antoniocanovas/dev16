# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = ['stock.picking']

    def action_open_picking_label_report_layout(self):
        return {
            'name': _("Report Wizard"),
            'view_mode': 'form',
            'view_id': self.env.ref('custom_azarey.stock_picking_wizard_view').id,
            'view_type': 'form',
            'res_model': 'stock.picking.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            # 'domain': '[if you need]',
            'context': {'default_pnt_picking_ids': self.ids}

        }