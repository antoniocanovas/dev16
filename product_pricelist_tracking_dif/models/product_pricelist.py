# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime,

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.depends('write_date')
    def update_pricelist_tracking(self):
        item_tracking = ""
        now = datetime.datetime.now()

        for li in self.item_ids:
            dif = (now - li.write_date).total_seconds()
            if dif < 3:
                name = li.product_tmpl_id.name
                if li.product_id.id: name = li.product_id.name
                item_tracking += "<p>" + name + ", Min.: " + str(li.min_quantity) + ", Price: " + str(li.fixed_price) + "</p>"

        if item_tracking != "":
            new_note = self.env['mail.message'].create({'body': tagtracking,
                                                        'message_type': 'comment',
                                                        'model': 'product.pricelist',
                                                        'res_id': self.id,
                                                        })
