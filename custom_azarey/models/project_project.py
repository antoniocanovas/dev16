# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = "project.project"

    def _pending_ean(self):
        total = 0
        product_without_ean = self.env["product.product"].search(
            [("shoes_campaign_id", "=", self.id), ("barcode", "=", False)]
        )
        if product_without_ean:
            total = len(product_without_ean)
        self.pnt_pending_ean = total

    pnt_pending_ean = fields.Integer(
        compute="_pending_ean", string="Pending EAN", store=False
    )

    def action_assign_ean_code(self):
        products = self.env["product.product"].search(
            [("shoes_campaign_id", "=", self.id)]
        )
        i = 0
        message = _("All products have EAN code")

        for product in products:
            if not product.barcode:
                i += 1
                info = product.with_context(
                    code="pnt.product.ean.code"
                ).create_default_code()
                if info:
                    info["params"]["message"] = (
                        _(
                            "Assigned %s EAN's, rest %s products, last product assigned: %s"
                        )
                        % (len(products),
                        self.pnt_pending_ean,
                        product.display_name,)
                    )
                    return info
        title = _("EAN codes assgined succesfully")
        if i != 0:
            message = _("%s EAN codes generated successfully") % i

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "sticky": False,
            },
        }
