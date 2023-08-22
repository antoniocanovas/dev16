from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupTemplateLine(models.Model):
    _name = 'wup.template.line'
    _description = 'Líneas de los productos en el set (wups):'

    template_id = fields.Many2one('wup.template', string='wup Template')
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity')
    product_uom = fields.Many2one('uom.uom', related='product_id.uom_id')
    sequence = fields.Integer('Sequence')

    @api.depends('product_id')
    def get_name_from_line_product_id(self):
        for record in self:
            record.name = record.product_id.name
    name = fields.Char(string='Name', store=True, readonly=False, compute="get_name_from_line_product_id")

