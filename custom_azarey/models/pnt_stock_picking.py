# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    dachser_document = fields.Binary("Label")
