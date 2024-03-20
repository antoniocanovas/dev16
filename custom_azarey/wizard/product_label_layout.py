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
        if self.custom_quantity <= 0:
            raise UserError(_("You need to set a positive quantity."))

        # Get layout grid
        if self.print_format == "dymo":
            xml_id = "product.report_product_template_label_dymo"
        elif "x" in self.print_format:
            if self.rows == 6 and self.columns == 5:
                xml_id = "custom_azarey.pnt_report_producttemplate_label"

            else:
                xml_id = "product.report_product_template_label"
        else:
            xml_id = ""

        active_model = ""
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            active_model = "product.template"
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = "product.product"
        else:
            raise UserError(
                _(
                    "No product to print, if the product is archived please unarchive it before printing its label."
                )
            )

        # Build data to pass to the report
        data = {
            "active_model": active_model,
            "quantity_by_product": {p: self.custom_quantity for p in products},
            "layout_wizard": self.id,
            "price_included": "xprice" in self.print_format,
        }
        return xml_id, data
