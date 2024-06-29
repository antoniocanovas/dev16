# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Comercialmente en cada pedido quieren saber cuántos pares se han facturado:
    @api.depends('product_id', 'quantity')
    def _get_shoes_invoice_line_pair_count(self):
        for record in self:
            record['pairs_count'] = record.product_id.pairs_count * record.quantity
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_invoice_line_pair_count')

    # Precio por par según tarifa:
    @api.depends('product_id','price_unit')
    def _get_shoes_invoice_pair_price(self):
        for record in self:
            total = 0
            if record.pairs_count != 0: total = record.price_subtotal / record.pairs_count
            record['pair_price'] = total
    pair_price = fields.Float('Pair price', store=True, compute='_get_shoes_invoice_pair_price')

    color_attribute_id = fields.Many2one('product.attribute.value', string='Color',
                                         store=True,
                                         related='product_id.color_attribute_id')

    size_attribute_id = fields.Many2one('product.attribute.value', string='Size',
                                         store=True,
                                         related='product_id.size_attribute_id')

    shoes_campaign_id = fields.Many2one('project.project', string='Shoes Campaign',
                                        store=True,
                                        related='product_id.shoes_campaign_id')
    shoes_model_id = fields.Many2one('product.template', store=True, related='product_id.shoes_model_id')
    exwork_single_euro = fields.Monetary(related="shoes_model_id.exwork_single_euro")

    @api.depends('price_subtotal', 'cost_price')
    def _get_shoes_margin(self):
        for record in self:
            record['shoes_margin'] = record.price_subtotal - record.cost_price

    shoes_margin = fields.Monetary('Margin', compute='_get_shoes_margin')

    @api.depends('shoes_margin', 'pairs_count')
    def _get_shoes_pair_margin(self):
        for record in self:
            shoes_pair_margin = record.shoes_pair_margin
            if record.pairs_count != 0:
                shoes_pair_margin = record.shoes_margin / record.pairs_count
            record['shoes_pair_margin'] = shoes_pair_margin

    shoes_pair_margin = fields.Monetary('Pair margin', compute='_get_shoes_pair_margin')


    @api.depends("price_unit")
    def _get_pair_price_sale(self):
        for record in self:
            price_pair_sale = record.price_subtotal
            if (record.pairs_count != 0) and (record.quantity):
                price_pair_sale = price_pair_sale / record.pairs_count
            record['pair_price_sale'] = price_pair_sale
    pair_price_sale = fields.Monetary("Pair price sale", compute="_get_pair_price_sale")

    @api.depends('exwork_single_euro', 'pairs_count')
    def _get_cost_price(self):
        for record in self:
            record.cost_price = record.pairs_count * record.exwork_single_euro

    cost_price = fields.Float("Cost price", compute="_get_cost_price")

    @api.depends('discount','price_unit')
    def _get_total_shoes_discount(self):
        for record in self:
            record['discount_amount'] = record.price_unit * record.quantity - record.price_subtotal
    discount_amount = fields.Monetary("Total discount", compute="_get_total_shoes_discount")

    manager_commission = fields.Monetary(
        string="Manager Commission", compute="_compute_account_move_line_manager_commission"
    )

    # ============= Pendiente de calcular por línea y hacer la parte proporcional del total origen:
    def _compute_account_move_line_manager_commission(self):
        self.manager_commission = 0
        # Una línea de facturación puede venir de distintos pedidos de venta y varias líneas del mismo pedido:
        for li in self.sale_line_ids:
            for so in li.order_id:
                if (
                        not so.referrer_id
                        or not so.commission_plan_id
                        or not so.manager_id
                        or not so.manager_commission_plan_id
                ):
                    so.manager_commission = 0
                else:
                    comm_by_rule = defaultdict(float)
                    template = so.sale_order_template_id
                    template_id = template.id if template else None
                    for line in so.order_line:
                        rule = so.manager_commission_plan_id._match_rules(
                            line.product_id, template_id, so.pricelist_id.id
                        )
                        # Añado al método estándar que la línea esté en el m2m consolidado:
                        if rule and li.id in self.sale_line_ids.ids:
                            manager_commission = so.currency_id.round(
                                line.price_subtotal * rule.rate / 100.0
                            )
                            comm_by_rule[rule] += manager_commission

                # cap by rule
                for r, amount in comm_by_rule.items():
                    if r.is_capped:
                        amount = min(amount, r.max_commission)
                        comm_by_rule[r] = amount

                self.manager_commission = sum(comm_by_rule.values())
