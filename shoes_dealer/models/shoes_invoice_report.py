# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api, _


# El objetivo es un informe agrupado por fecha(día) / Cliente / Modelo
# así que necesitamos las líneas oportunas con todos los datos, considerando líneas facturadas y abonos.
# Si conseguimos estas líneas, un pivot ¿podría sacar esta información?


class ShoesInvoiceReport(models.Model):
    _name = "shoes.invoice.report"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Shoes Invoice Report"

    name = fields.Char(string="Nombre", required=True)
    shoes_campaign_id = fields.Many2one("project.project", string="Shoes campaign")

    pairs_count = fields.Integer("Pairs count")
    from_date = fields.Date("From date")
    to_date = fields.Date("To date")
    invoice_amount = fields.Monetary('Invoiced')
    margin_amount = fields.Monetary('Margin')
    currency_id = fields.Many2one('res.currency', default=lambda self.company.currency_id)

class ShoesInvoiceReportLine(models.Model):
    _name = "shoes.invoice.report.line"
    _description = "Shoes Invoice Report Line"

    # ¿Qué pasa si la línea de factura cambia? ... api.depends
    move_line_id = fields.Many2one('account.move.line', string="Invoice line")


    model_id = fields.Many2one('product.template', string='Model', compute='_get_shoes_model')
    name = fields.Char("Model", related="model_id.name", store=True, help="Pair or assortment invoiced")
    shoes_campaign_id = fields.Many2one("project.project", store=True, string="Shoes campaign", related='move_line_id.product_id.shoes_campaign_id')
    partner_id = fields.Many2one('res.partner', store=True, string="Customer", related='move_line_id.partner_id')

    pairs_count = fields.Integer("Pairs count", store=True, related='move_line_id.pairs_count')
    pair_exwork = fields.Monetary("Pair exwork", store=True, related='model_id.exwork_single')
    price_pair = fields.Monetary("Pair price", store=True, related='model.product_tmpl_single_list_price')

    # Voy por aquí:
    discount_pair = fields.Float("Pair discount")
    discount_amount = fields.Monetary("Discount")
    commission_pair = fields.Monetary("Pair commission")
    commission_amount = fields.Monetary("Commission")
    price_pair_discount = fields.Monetary("Pair net price")
    price_amount = fields.Monetary("Net price")
    margin_pair = fields.Monetary("Pair margin")
    margin_amount = fields.Monetary("Margin")
    currency_id = fields.Many2one('res.currency', default=lambda self.company.currency_id)

    @api.depends('move_line_id.product_id')
    def _get_shoes_model(self):
        for record in self:
            model = False
            if record.move_line_id.product_id.product_tmpl_id.is_assortment:
                model = record.move_line_id.product_id.product_tmpl_id.id
            elif record.move_line_id.product_id.product_tmpl_id.is_pair:
                model = record.move_line_id.product_id.product_tmpl_id.product_tmpl_set_id.id
            record.model_id = model

