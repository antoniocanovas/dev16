# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']

    pnt_campaign_id = fields.Many2one('project.project', string='Campaign', store=True, copy=False, tracking=16)
    pnt_pre_margin_amount = fields.Monetary('Pre margin', store=True, copy=True, tracking=16)
    pnt_landed_amount = fields.Monetary('Landed cost', store=True, copy=True, tracking=16)
    pnt_margin = fields.Float('Margin %', store=True, copy=True, tracking=16)
    pnt_post_margin_amount = fields.Monetary('Post margin', store=True, copy=True, tracking=16)
    pnt_product_brand_id = fields.Many2one('product.brand', string='Brand', store=True, copy=True, tracking=16)

    pnt_product_tmpl_item_ids = fields.One2many('product.pricelist.item', 'pricelist_id',
                                                domain=[('applied_on','=','1_product')]
                                                )

    @api.depends('item_ids')
    def _get_pricelist_product_tmpl(self):
        templates = []
        for li in self.item_ids:
            if li.product_tmpl_id.id not in templates:
                templates.append(li.product_id.product_tmpl_id.id)
        self.pnt_product_tmpl_ids = [(6, 0, templates)]
    pnt_product_tmpl_ids = fields.Many2many('product.template', string='Product templates', store=False,
                                            compute='_get_pricelist_product_tmpl')

    def products_pricelist_recalculation_by_campaign(self):
        for record in self:
            # Pares sueltos (tarifa por plantilla de producto):
            pairs = self.env['product.product'].search([('product_tmpl_set_id', '!=', False),
                                                        ('campaign_id', '=', record.pnt_campaign_id.id),
                                                        ('product_brand_id','=', record.pnt_product_brand_id.id)
                                                        ])
            pair_templates = []
            pre_margin = record.pnt_pre_margin_amount
            landed = record.pnt_landed_amount
            margin = record.pnt_margin
            post_margin = record.pnt_post_margin_amount

            # Pricelist item deletion to avoid old prices of pairs changed of campaign:
            record.item_ids.unlink()

            for pr in pairs:
                price = pr.lst_price
                pr.write({'standard_price': pr.exwork + pr.shipping_price})
                total = (price + pre_margin + landed) * (1 + margin / 100) + post_margin
                if pr.product_tmpl_id.id not in pair_templates:
                    # Creamos una línea nueva:
                    pricelist_line = self.env['product.pricelist.item'].create({'pricelist_id': record.id,
                                                                                'product_tmpl_id': pr.product_tmpl_id.id,
                                                                                'compute_price': 'fixed',
                                                                                'applied_on': '1_product',
                                                                                'product_id': False,
                                                                                'fixed_price': total})

                    # Añadimos al array para que no escriba lo mismo:
                    pair_templates.append(pr.product_tmpl_id.id)

            # Surtidos (tarifa por producto):
            sets = self.env['product.product'].search([('product_tmpl_single_id', '!=', False),
                                                       ('campaign_id', '=', record.pnt_campaign_id.id),
                                                       ('product_brand_id','=', record.pnt_product_brand_id.id)
                                                       ])
            for pr in sets:
                product_bom = self.env['mrp.bom'].search([('product_id', '=', pr.id)])
                if not product_bom.bom_line_ids.ids:
                    message = pr.name + " has no Bill of Materials, please review and press CREATE PAIRS"
                    raise UserError(message)
# ELIMINADO 27/11/23 (error recálculo precios base)                else:
#                    single = product_bom[0].product_id
#                # Actualizar el precio del set en base al producto anterior ¿Para qué? HABLAMOS DE TARIFAS:
#                pr.write({'lst_price': single.lst_price * pr.pairs_count,
#                          'standard_price': single.standard_price * pr.pairs_count})

                # Crear líneas de tarifa (podría haber valido la búsqueda anterior??):
                single_price = pr.product_tmpl_single_id.list_price
                total =  pr.pairs_count * ((single_price + pre_margin + landed) * (1 + margin / 100) + post_margin)

                # Creamos una línea nueva:
                pricelist_line = self.env['product.pricelist.item'].create({'pricelist_id': record.id,
                                                                            'product_tmpl_id': pr.product_tmpl_id.id,
                                                                            'product_id': pr.id,
                                                                            'compute_price': 'fixed',
                                                                            'applied_on': '0_product_variant',
                                                                            'fixed_price': total})

    def call_report_wizard(self):

        return {
            'name': _("Report Wizard"),
            'view_mode': 'form',
            'view_id': self.env.ref('custom_azarey.product_pricelist_wizard_view').id,
            'view_type': 'form',
            'res_model': 'product.pricelist.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            #'domain': '[if you need]',
            'context': {'default_pnt_product_pricelist_id': self.id}
        }