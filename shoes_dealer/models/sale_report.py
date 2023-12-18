# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleReport(models.Model):
    _inherit = "sale.report"

    # Informes de ventas:
    def _get_shoes_pair_count(self):
        for record in self:
            pairs_count = 1
            if record.product_id.pairs_count: pairs_count = record.product_id.pairs_count
            record['pairs_count'] = pairs_count * record.product_uom_qty
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_pair_count')

    @api.depends('product_id')
    def get_sale_report_color(self):
        for record in self:
            color_attribute = self.env.user.company_id.color_attribute_id

            # Para buscar el color:
            color_value = self.env['product.template.attribute.value'].search([
                ('product_tmpl_id', '=', record.product_tmpl_id.id),
                ('id', 'in', record.product_id.product_template_variant_value_ids.ids),
                ('attribute_id', '=', color_attribute.id)]).product_attribute_value_id

            # Caso de que sólo haya un COLOR, no existe el registro anterior PTAV, buscamos en la línea atributo de PT:
            if not color_value.id:
                color_value = self.env['product.template.attribute.line'].search([
                    ('product_tmpl_id', '=', record.product_tmpl_id.id),
                    ('attribute_id', '=', color_attribute.id)]).product_template_value_ids[0].product_attribute_value_id
            record['color_id'] = color_value.id
    color_id = fields.Many2one('product.attribute.value', string='Color', store=True, compute='get_sale_report_color')