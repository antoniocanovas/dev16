from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.depends('item_ids.product_tmpl_id')
    def _get_pricelist_products(self):
        products = []
        for li in self.item_ids:
            if (li.product_tmpl_id.id) and not (li.product_id.id):
                product_ids = self.env['product.product'].search([('product_tmpl_id', '=', li.product_tmpl_id.id)])
                for pro in product_ids: products.append(pro.id)
            else:
                products.append(li.product_id.id)
        self.product_ids = [(6,0,products)]
    product_ids = fields.Many2many('product.product', store=True, compute='_get_pricelist_products')



    # Recalcular precios de tarifa en base a parámetros establecidos:
    def products_pricelist_recalculation(self):
        # Pendiente de desarrollo !!!!
        return True



    # Crear una nota con los precios que han cambiado en la tarifa, desde botón o acción planificada:
    def pricelist_tracking(self):
        item_tracking = ""
        now = datetime.now()

        for li in self.item_ids:
            if not(li.tracking_date) or (li.tracking_date < li.write_date):
                name = li.product_tmpl_id.name
                if li.product_id.id: name = li.product_id.name
                item_tracking += "<p>" + name + ", Min.: " + str(li.min_quantity) + ", Price: " + str(li.fixed_price) + "</p>"
                li.tracking_date = now

        if item_tracking != "":
            new_note = self.env['mail.message'].create({'body': item_tracking,
                                                        'message_type': 'comment',
                                                        'model': 'product.pricelist',
                                                        'res_id': self.id,
                                                        })