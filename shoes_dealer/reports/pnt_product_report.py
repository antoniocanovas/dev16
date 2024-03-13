from odoo import _, api, fields, models
from odoo.exceptions import UserError


def _prepare_data(env, data):
    if data.get("active_model") == "product.template":
        product = env["product.template"]
    else:
        raise UserError(_("Model not defined, Please contact your administrator."))

    product_ids = data.get("product_ids")
    products = product.search([("id", "in", product_ids)], order="pnt_sales_count desc")
    layout_wizard = env["product.report.wizard"].browse(data.get("layout_wizard"))

    if not layout_wizard:
        return {}
    else:
        report = layout_wizard.pnt_product_report_template
    return {
        "products": products,
        "product_number": len(products),
        "report": report,
    }


class ProjectTopReport(models.AbstractModel):
    _name = "report.shoes_dealer.product_top_report"
    _description = "Reporting engine for products"

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)
