from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupTemplate(models.Model):
    _name = 'wup.template'
    _description = 'wup Template'

    name = fields.Char(string='Name',  store=True)
    ref = fields.Char(string='Ref',  store=True)
    description = fields.Text(string='Description',  store=True)
    department_id = fields.Many2one('hr.department', string='Department',  store=True)
    target_id = fields.Many2one('wup.target', help='Office, Residential', string='Target',  store=True)
    quality_id = fields.Many2one('wup.quality', string='Quality',  store=True)
    style_id = fields.Many2one('wup.style', string='Style',  store=True)
    type_id = fields.Many2one('wup.type',  string='Type',  store=True)
    product_brand_id = fields.Many2one('product.brand', string='Product brand',  store=True)

    line_ids = fields.One2many('wup.template.line', 'template_id', string='Line', store=True, copy=True)
