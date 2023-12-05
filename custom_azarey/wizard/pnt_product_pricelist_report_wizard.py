import base64
import codecs
from PIL import Image
import io
from odoo import fields, models, api
from odoo.exceptions import ValidationError

REPORT_TYPE = [
    ('pnt_model_pricelist_report', 'Models'),
    ('not', 'NOT'),
    ('dont', 'DONT'),
]

class ProductPricelistReportWizard(models.TransientModel):
    _name = 'product.pricelist.report.wizard'
    _description = 'Reporting engine for product pricelist'


    name = fields.Char('Name')
    pnt_report_template = fields.Selection(
        selection=REPORT_TYPE,
        string="Report Type",
        default='pnt_model_pricelist_report',)
    pnt_product_pricelist_id = fields.Many2one('product.pricelist', string="Product pricelist")

    def print_product_pricelist_report(self):
        #data = {'description_sale': 'Nueva Descripción'}
        #print(self.pnt_product_pricelist_id)
        #query = """select pr.name,fv.name as truck,gt.name as goods,tb.from_location,tb.to_location,tb.distance,
        #                tb.weight,tb.unit,amount,tb.date,tb.state from truck_booking as tb
        #                inner join res_partner as pr on pr.id = tb.partner_id
        #                inner join fleet_vehicle_model as fv on fv.id = tb.truck_id
        #                inner join goods_type as gt on gt.id = tb.goods_type_id """
        #if self.from_date:
        #    query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date
        #self.env.cr.execute(query)
        #report = self.env.cr.dictfetchall()
        #data = {'date': self.read()[0], 'report': report}
        #return self.env.ref('custom_azarey.pricelist_report').report_action(None, data=data)
        return self.env.ref('custom_azarey.pnt_model_pricelist_report').report_action(self.pnt_product_pricelist_id.id)