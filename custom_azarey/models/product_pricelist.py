# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductPricelist(models.Model):
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']
#    _inherit = ['product.pricelist']

    pnt_campaign_id = fields.Many2one('project.project', string='Campaign', store=True, copy=False, tracking='1')
    pnt_pre_margin_amount = fields.Monetary('Pre margin', store=True, copy=True, tracking='1')
    pnt_landed_amount = fields.Monetary('Landed cost', store=True, copy=True, tracking='1')
    pnt_margin = fields.Float('Margin %', store=True, copy=True, tracking='1')
    pnt_post_margin_amount = fields.Monetary('Post margin', store=True, copy=True, tracking='1')

    def campaing_products_pricelist_recalculation(self):
        products = self.env['product.template'].search([('campaign_id','=', self.pnt_campaign_id.id)])
        # HAY QUE PONER PRECIOS A LOS PRODUCTOS, NO A LAS PLANTILLAS, EN LOS SURTIDOS DEPENDEMOS DEL Nº DE PARES

        for pt in products:
            pair = pt.product_tmpl_single_id.id
            if pair.id:         # Es un surtido, precio distinto por producto.
                for pr in pt.product_variant_ids:
                    # Cálculo del precio para la tarifa:
                    total = ((pair.list_price + self.pnt_pre_margin_amount + self.pnt_landed_amount) * \
                             (1 + self.pnt_margin / 100) + self.pnt_post_margin_amount) * pr.pairs_count

            # Si es un surtido, tiene "product_tmpl_single_id" => el precio es el del par que lo compone.
            price = pr.list_price
            if (pr.product_tmpl_single_id.id):
                price = pr.product_tmpl_single_id.id
            # Cálculo del precio para la trifa:
            total = ((price + self.pnt_pre_margin_amount + self.pnt_landed_amount) * \
                    (1 + self.pnt_margin/100) + self.pnt_post_margin_amount) * pr.pairs_count
            # Vemos si ya existe el producto en esta tarifa:
            pricelist_line = self.env['product.pricelist.item'].search([('pricelist_id','=', self.id),
                                                                        ('product_tmpl_id','=', pr.id)])
            # Si no existe creamos una línea nueva:
            if not pricelist_line.id:
                pricelist_line = self.env['product.pricelist.item'].create({'pricelist_id': self.id,
                                                                            'product_tmpl_id': pr.id,
                                                                            'compute_price':'fixed',
                                                                            'applied_on':'1_product',
                                                                            'fixed_price':total})
            # Si existe la actualizamos:
            else:
                pricelist_line.write({'pricelist_id': self.id,
                                      'product_tmpl_id': pr.id,
                                      'compute_price': 'fixed',
                                      'applied_on': '1_product',
                                      'fixed_price': total})