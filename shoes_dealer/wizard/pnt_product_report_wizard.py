from odoo import _, api, fields, models
from odoo.exceptions import UserError


REPORT_TYPE = [
    ("top", "TOP"),
]


class ProductProductReportWizard(models.TransientModel):
    _name = "product.report.wizard"
    _description = "Reporting engine for product product"

    pnt_product_report_template = fields.Selection(
        selection=REPORT_TYPE,
        string="Report Type",
        default="top",
    )
    pnt_campaign_id = fields.Many2one(
        "project.project",
        string="Campaign",
    )

    def _prepare_report_data(self):
        xml_id = "shoes_dealer.pnt_model_product_top_report"
        # Build data to pass to the report
        product_ids = self.env["product.template"].search(
            [
                ("shoes_campaign_id", "=", self.pnt_campaign_id.id),
                ("pnt_sales_count", ">", 0),
            ]
        )

        data = {
            "active_model": "product.template",
            "product_ids": product_ids.ids,
            "layout_wizard": self.id,
        }
        return xml_id, data

    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(
                _(
                    "Unable to find report template for %s format",
                    self.pnt_product_report_template,
                )
            )
        report_action = self.env.ref(xml_id).report_action(None, data=data)
        report_action.update({"close_on_report_download": True})
        return report_action
