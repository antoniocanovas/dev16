from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'sale.order'

    def name_get(self):
        result = []
        for order in self:
            name = order.name
            if order.client_order_ref:
                name += ' - ' + order.client_order_ref
            result.append((order.id, name))
        return result
