from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[
            ("5x6", "5 x 6"),
            ("5x6xprice", "5 x 6 with price"),
        ],
        default="5x6",
        ondelete={
            "5x6": "set default",
            "5x6xprice": "set default",
        },
    )

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if "x" in self.print_format:
            if self.rows == 6 and self.columns == 5:
                xml_id = "custom_azarey.pnt_report_producttemplate_label"

        return xml_id, data
