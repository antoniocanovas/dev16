
from odoo import _, api, fields, models
from odoo.exceptions import UserError



REPORT_TYPE = [
    ('external', 'External'),
]

class StockPickingReportWizard(models.TransientModel):
    _name = 'stock.picking.report.wizard'
    _description = 'Reporting engine for stock picking external labels'

    pnt_stock_picking_report_template = fields.Selection(
        selection=REPORT_TYPE,
        string="Report Type",
        default='external',)
    pnt_picking_ids = fields.Many2many('stock.picking', string="Picking")
    pnt_parcels = fields.Integer('Parcels')

    def _prepare_report_data(self):

        xml_id = 'custom_azarey.pnt_report_stock_picking_label'

        # Build data to pass to the report
        data = {
            'active_model': 'stock.picking',
            'picking_ids': self.pnt_picking_ids.ids,
            'layout_wizard': self.id,
        }
        return xml_id, data

    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(
                _('Unable to find report template for %s format', self.pnt_stock_picking_report_template))
        report_action = self.env.ref(xml_id).report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action