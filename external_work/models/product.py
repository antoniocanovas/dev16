from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends('type','uom_id')
    def _get_is_work_time(self):
        for record in self:
            is_work_time = False
            wtime_category = record.env['ir.model.data'].search([('model','=','uom.category'),('name','=','uom_categ_wtime')])
            if (record.uom_id.category_id.id == wtime_category.res_id): is_work_time = True
            record['is_work_time'] = is_work_time
    is_work_time = fields.Boolean('Is working time', store=True, compute=_get_is_work_time)
