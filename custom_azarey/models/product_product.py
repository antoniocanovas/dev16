# Copyright Punt Sistemes SL - PUNT

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
import zipfile
from io import BytesIO
import base64
from gtin import GTIN


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Impedir archivar productos si tienen pedidos de venta:
    pnt_sale_line_ids = fields.One2many(
        "sale.order.line", "product_id", string="Sale lines", store=True, copy=False
    )

    @api.depends("name")
    def _get_pnt_image_name(self):
        for record in self:
            name_image = record.name
            for li in record.product_template_attribute_value_ids:
                att = li.display_name.split(":")[0]
                if att == "Color":
                    name_image += "_" + li.name
                elif att == "Surtido":
                    name_image += "_" + li.name.split("(")[0]
            record["pnt_image_name"] = name_image.strip()

    pnt_image_name = fields.Char(
        "Image name",
        compute="_get_pnt_image_name",
        help="Nombre del fichero imagen exportado para marketing / Prestashop",
    )

    @api.constrains("active")
    def _avoid_archive_sold_products(self):
        for record in self:
            if (record.active == False) and (record.pnt_sale_line_ids.ids):
                raise UserError("Remove sale lines before archiving !!")
            if (record.active == False) and (record.purchase_order_line_ids.ids):
                raise UserError("Remove purchase lines before archiving !!")

    def delete_product_archived_in_sale_line(self):
        for li in self.pnt_sale_line_ids:
            if li.product_id.id == self.id:
                if li.state == "done":
                    message = (
                        "Confirmed sales order must be cancelled and set to RESERVATION before: "
                        + li.order_id.name
                    )
                    raise UserError(message)
                else:
                    name = (
                        li.product_id.name
                        + ", cantidad: "
                        + str(li.product_uom_qty)
                        + " => Cancelado el "
                        + str(date.today())
                    )
                    newnote = self.env["sale.order.line"].create(
                        {
                            "display_type": "line_note",
                            "name": name,
                            "order_id": li.order_id.id,
                        }
                    )
                    li.unlink()

    def action_product_iamges_download(self):
        items = self.filtered(lambda x: x.image_1920 != False)
        if not items:
            raise UserError(
                _("None attachment selected. Only binary attachments allowed.")
            )
        ids = ",".join(map(str, items.ids))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/products/download_zip?ids=%s" % (ids),
            "target": "self",
        }

    def _create_temp_zip(self):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for product in self:
                zip_file.writestr(
                    str(product.pnt_image_name) + ".jpg",
                    base64.decodebytes(product.image_1920),
                )
            zip_buffer.seek(0)
            zip_file.close()
        return zip_buffer

    @api.depends_context("display_default_code", "seller_id")
    def name_get(self):
        result = super().name_get()
        custom = []

        def custom_get_name(d):
            name = d.get("name", "")
            return (d["id"], name)

        for product in result:
            id = product[0]
            product_to_modify = self.search([("id", "=", id)])

            name = product[1]

            atcolor = self.env.company.color_attribute_id
            ptal = self.env["product.template.attribute.line"].search(
                [
                    ("product_tmpl_id", "=", product_to_modify.product_tmpl_id.id),
                    ("attribute_id", "=", atcolor.id),
                ]
            )
            if (ptal.value_ids.ids) and (len(ptal.value_ids) == 1):
                name += " " + str(ptal.value_ids[0].name)

            atbom = self.env.company.bom_attribute_id
            ptal = self.env["product.template.attribute.line"].search(
                [
                    ("product_tmpl_id", "=", product_to_modify.product_tmpl_id.id),
                    ("attribute_id", "=", atbom.id),
                ]
            )
            if (ptal.value_ids.ids) and (len(ptal.value_ids) == 1):
                name += " " + str(ptal.value_ids[0].name)
            mydict = {
                "id": product_to_modify.id,
                "name": name,
            }
            custom.append(custom_get_name(mydict))
        return custom

    def create_default_code(self):
        code = self.env.context.get("code")
        seq = self.env["ir.sequence"].search([("code", "=", code)], limit=1)
        pnt_ean14_prefix = seq.pnt_ean14_prefix

        for product in self:
            if not product.barcode:
                sequence = self.env["ir.sequence"].search([("code", "=", code)])
                barcode = self.env["ir.sequence"].next_by_code(code)
                clean_max_code_limit = barcode[-sequence.padding :].lstrip("0")

                if sequence.pnt_ean_code_limit == 0:
                    return {
                        "type": "ir.actions.client",
                        "tag": "display_notification",
                        "params": {
                            "title": _("Max codes set up"),
                            "message": _("Max codes limit mut be greater than '0'"),
                            "sticky": False,
                        },
                    }

                if (
                    str(clean_max_code_limit) == str(sequence.pnt_ean_code_limit)
                    or sequence.number_next_actual > sequence.pnt_ean_code_limit
                ):
                    return {
                        "type": "ir.actions.client",
                        "tag": "display_notification",
                        "params": {
                            "title": _(
                                "No EAN codes availlable on sequence, please update sequence"
                            ),
                            "message": _(
                                "The product %s EAN code did not assigned successfully"
                            )
                            % product.display_name,
                            "sticky": False,
                        },
                    }
                elif len(barcode) == 12:
                    if pnt_ean14_prefix and product.is_assortment:
                        barcode = (
                            str(pnt_ean14_prefix)
                            + str(barcode)
                            + str(GTIN(raw=str(barcode)).check_digit)
                        )
                        super(ProductProduct, self).write({"barcode": barcode})
                    else:
                        barcode = str(barcode) + str(GTIN(raw=str(barcode)).check_digit)
                        super(ProductProduct, self).write({"barcode": barcode})
                else:
                    raise UserError(
                        _("The product %s does not have an EAN length")
                        % product.display_name
                    )
