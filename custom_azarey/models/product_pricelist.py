# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductPricelist(models.Model):
    #    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']
    _inherit = ['product.pricelist']

    pnt_campaign_id = fields.Many2one('project.project', string='Campaign', store=True, copy=False, tracking=16)
    pnt_pre_margin_amount = fields.Monetary('Pre margin', store=True, copy=True, tracking=16)
    pnt_landed_amount = fields.Monetary('Landed cost', store=True, copy=True, tracking=16)
    pnt_margin = fields.Float('Margin %', store=True, copy=True, tracking=16)
    pnt_post_margin_amount = fields.Monetary('Post margin', store=True, copy=True, tracking=16)

    @api.depends('item_ids')
    def _get_pricelist_product_tmpl(self):
        templates = []
        for li in self.item_ids:
            if li.product_tmpl_id.id not in templates:
                templates.append(li.product_id.product_tmpl_id.id)
        self.product_tmpl_ids = [(6, 0, templates)]
    pnt_product_tmpl_ids = fields.Many2many('product.template', string='Product templates', store=False,
                                            compute='_get_pricelist_product_tmpl')

    def products_pricelist_recalculation_by_campaign(self):
        for record in self:
            # Pares sueltos (tarifa por plantilla de producto):
            pairs = self.env['product.product'].search([('product_tmpl_set_id', '!=', False), ('campaign_id', '=', record.pnt_campaign_id.id)])
            pair_templates = []
            for pr in pairs:
                price = pr.lst_price
                pr.write({'standard_price': pr.exwork + pr.shipping_price})
                total = (price + record.pnt_pre_margin_amount + record.pnt_landed_amount) * (1 + record.pnt_margin / 100) + record.pnt_post_margin_amount
                if pr.product_tmpl_id.id not in pair_templates:
                    pricelist_line = self.env['product.pricelist.item'].search([('pricelist_id', '=', record.id),
                                                                                ('product_tmpl_id', '=', pr.product_tmpl_id.id)])
                    # Si no existe creamos una línea nueva:
                    if not pricelist_line.id:
                        pricelist_line = self.env['product.pricelist.item'].create({'pricelist_id': record.id,
                                                                                    'product_tmpl_id': pr.product_tmpl_id.id,
                                                                                    'compute_price': 'fixed',
                                                                                    'applied_on': '1_product',
                                                                                    'product_id': False,
                                                                                    'fixed_price': total})
                    # Si existe la actualizamos:
                    else:
                        pricelist_line.write({'product_id': False,
                                              'compute_price': 'fixed',
                                              'applied_on': '1_product',
                                              'fixed_price': total})

                    # Añadimos al array para que no escriba lo mismo:
                    pair_templates.append(pr.product_tmpl_id.id)

            # Surtidos (tarifa por producto):
            sets = self.env['product.product'].search(
                [('product_tmpl_single_id', '!=', False), ('campaign_id', '=', record.pnt_campaign_id.id)])
            for pr in sets:
                single_standard_price = self.env['mrp.bom'].search([('product_id', '=', pr.id)]).bom_line_ids[0].product_id.standard_price
                price = pr.product_tmpl_single_id.list_price * pr.pairs_count
                pr.write({'lst_price': price, 'standard_price': single_standard_price * pr.pairs_count})
                total = (price + record.pnt_pre_margin_amount + record.pnt_landed_amount) * (1 + record.pnt_margin / 100) + record.pnt_post_margin_amount

                # Vemos si ya existe el producto en esta tarifa:
                pricelist_line = self.env['product.pricelist.item'].search([('pricelist_id', '=', record.id),
                                                                            ('product_id', '=', pr.id)])
                # Si no existe creamos una línea nueva:
                if not pricelist_line.id:
                    pricelist_line = self.env['product.pricelist.item'].create({'pricelist_id': record.id,
                                                                                'product_tmpl_id': pr.product_tmpl_id.id,
                                                                                'product_id': pr.id,
                                                                                'compute_price': 'fixed',
                                                                                'applied_on': '0_product_variant',
                                                                                'fixed_price': total})
                # Si existe la actualizamos:
                else:
                    pricelist_line.write({'compute_price': 'fixed',
                                          'applied_on': '1_product',
                                          'fixed_price': total})