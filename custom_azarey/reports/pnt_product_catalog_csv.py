import csv
from odoo import models


class ProductCatalogCSV(models.AbstractModel):
    _name = "report.custom_azarey.product_catalog_csv"
    _inherit = "report.report_csv.abstract"

    def generate_csv_report(self, writer, data, products):
        writer.writeheader()
        bom_attribute = self.env.user.company_id.bom_attribute_id
        color_attribute = self.env.user.company_id.color_attribute_id
        for r in products:
            pair_price = r.product_tmpl_single_id.list_price
            ptal = self.env["product.template.attribute.line"].search(
                [
                    ("attribute_id", "=", color_attribute.id),
                    ("product_tmpl_id", "=", r.id),
                ]
            )
            ptal_colors = ptal.value_ids
            color = []
            image = []
            if len(ptal_colors) == 1:
                color.append(ptal_colors[0].name)
                image.append(str(r.name) + str(ptal_colors[0].name) + ".jpg")
            else:
                # Bucle para sacar cada color y url de su imagen:
                for li in ptal_colors:
                    # Necesito un pp de ese color para sacar la foto, para ello desde value => ptav => pp.ids:
                    ptav = self.env["product.template.attribute.value"].search(
                        [
                            ("product_attribute_value_id", "=", li.id),
                            ("product_tmpl_id", "=", r.id),
                        ]
                    )
                    pp = self.env["product.product"].search(
                        [
                            ("product_tmpl_id", "=", r.id),
                            ("product_template_variant_value_ids", "in", ptav.id),
                        ]
                    )
                    if pp.ids:
                        color.append(li.name)
                        image.append(str(pp[0].pnt_image_name) + ".jpg")

            writer.writerow(
                {
                    "modelo": r.name,
                    "precio": pair_price,
                    "color1": color[0] if 0 < len(color) else "",
                    "imagen1": image[0] if 0 < len(image) else "",
                    "color2": color[1] if 1 < len(color) else "",
                    "imagen2": image[1] if 1 < len(image) else "",
                    "color3": color[2] if 2 < len(color) else "",
                    "imagen3": image[2] if 2 < len(image) else "",
                    "color4": color[3] if 3 < len(color) else "",
                    "imagen4": image[3] if 3 < len(image) else "",
                    "color5": color[4] if 4 < len(color) else "",
                    "imagen5": image[4] if 4 < len(image) else "",
                    "color6": color[5] if 5 < len(color) else "",
                    "imagen6": image[5] if 5 < len(image) else "",
                    "color7": color[6] if 6 < len(color) else "",
                    "imagen7": image[6] if 6 < len(image) else "",
                    "color8": color[7] if 7 < len(color) else "",
                    "imagen8": image[7] if 7 < len(image) else "",
                    "color9": color[8] if 8 < len(color) else "",
                    "imagen9": image[8] if 8 < len(image) else "",
                }
            )

    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("modelo")
        res["fieldnames"].append("precio")
        res["fieldnames"].append("color1")
        res["fieldnames"].append("imagen1")
        res["fieldnames"].append("color2")
        res["fieldnames"].append("imagen2")
        res["fieldnames"].append("color3")
        res["fieldnames"].append("imagen3")
        res["fieldnames"].append("color4")
        res["fieldnames"].append("imagen4")
        res["fieldnames"].append("color5")
        res["fieldnames"].append("imagen5")
        res["fieldnames"].append("color6")
        res["fieldnames"].append("imagen6")
        res["fieldnames"].append("color7")
        res["fieldnames"].append("imagen7")
        res["fieldnames"].append("color8")
        res["fieldnames"].append("imagen8")
        res["fieldnames"].append("color9")
        res["fieldnames"].append("imagen9")
        res["delimiter"] = ";"
        res["quoting"] = csv.QUOTE_ALL
        return res
