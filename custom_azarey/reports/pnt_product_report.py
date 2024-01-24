
from collections import defaultdict
import math
from odoo.exceptions import UserError

from odoo import _, api, fields, models
from odoo.exceptions import UserError

def _prepare_data(env, data):
    if data.get('active_model') == 'product.product':
        product = env['product.product']
    else:
        raise UserError(_('Model not defined, Please contact your administrator.'))

    product_ids = data.get('product_ids')
    products = product.search([('id', 'in', product_ids)], order='name desc')
    product_number = len(products)
    layout_wizard = env['product.report.wizard'].browse(data.get('layout_wizard'))

    if not layout_wizard:
        return {}
    else:
        report = layout_wizard.pnt_product_report_template
        print("DEBUG", report)
    return {
        'products': products,
        'product_number': product_number,
        'report': report,
    }

class ProjectMultiReport(models.AbstractModel):
    _name = 'report.custom_azarey.product_multi_report'
    _description = 'Reporting engine for products'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)
