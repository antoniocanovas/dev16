# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    # Comercialmente en cada pedido quieren saber cuántos pares se han facturado:
    amount_undiscounted = fields.Float(
        string="Amount Before Discount",
        compute="_compute_amount_undiscounted",
        digits=0,
    )

    def _compute_amount_undiscounted(self):
        for invoice in self:
            total = 0.0
            for line in invoice.invoice_line_ids:
                total += (
                    (line.price_subtotal * 100) / (100 - line.discount)
                    if line.discount != 100
                    else (line.price_unit * line.product_uom_qty)
                )
            invoice.amount_undiscounted = total
