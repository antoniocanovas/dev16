# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ShoesSaleReport(models.Model):
    _name = "shoes.sale.report"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Shoes Sale Report"

    name = fields.Char(string="Nombre", required=True)
    shoes_campaign_id = fields.Many2one("project.project", string="Shoes campaign")
    type = fields.Selection(
        [("model", "Model"), ("sale", "Sale")], string="Type", copy=True
    )
    pairs_count = fields.Integer("Pairs count")
    from_date = fields.Date("From date")
    to_date = fields.Date("To date")

    referrer_ids = fields.Many2many(comodel_name='res.partner',
                                    string="Referrers",
                                    relation="shoesreport_referrer_rel",
                                    domain=[("commission_plan_id", "!=", False)],
                                    context={'active_test': True},
                                    )
    partner_ids = fields.Many2many(comodel_name='res.partner',
                                   string="Customers",
                                   relation="shoesreport_customer_rel",
                                   domain=[("customer_rank", ">", 0)],
                                   context={'active_test': True},
                                   )

    order_ids = fields.Many2many("sale.order")
    product_ids = fields.Many2many("product.template", domain=[("sale_ok", "=", True)])
    model_ids = fields.One2many(
        "shoes.sale.report.line", "shoes_report_id", string="Lines"
    )

    @api.depends("shoes_campaign_id")
    def _get_sale_orders(self):
        for record in self:
            orders = []
            if record.type == "sale":
                all_orders = (self.env["sale.order"].search([
                    ("shoes_campaign_id", "=", record.shoes_campaign_id.id),
                    ("state", "not in", ["draft", "cancel"]),]))
                for order in all_orders:
                    if (record.from_date) and (order.date_order.date() < record.from_date): continue
                    if (record.to_date) and (order.date_order.date() > record.to_date): continue
                    if (record.referrer_ids.ids) and (order.referrer_id.id not in record.referrer_ids.ids): continue
                    if (record.partner_ids.ids) and (order.partner_id.id not in record.partner_ids.ids): continue
                    if (record.order_ids.ids) and (order.id not in record.order_ids.ids): continue
                    orders.append(order.id)
            record["sale_ids"] = [(6, 0, orders)]
    sale_ids = fields.Many2many(
        "sale.order", string="Orders", store=False, compute="_get_sale_orders"
    )

    def update_shoes_model_report(self):
        for record in self:
            # La información está en las líneas de venta agrupadas por modelo:
            sol = self.env["sale.order.line"].search(
                [("shoes_campaign_id", "=", record.shoes_campaign_id.id)]
            )
            record.model_ids.unlink()
            models, total_pairs = [], 0
            for li in sol:
                if (li.product_id.is_assortment or li.product_id.is_pair) and (
                        li.product_id.product_tmpl_id not in models
                ):
                    models.append(li.product_tmpl_id)

            for model in models:
                colors, total_model_pairs = [], 0
                lines = self.env["sale.order.line"].search(
                    [
                        ("shoes_campaign_id", "=", record.shoes_campaign_id.id),
                        ("product_tmpl_id", "=", model.id),
                    ]
                )
                for li in lines:
                    if li.product_id.color_attribute_id not in colors:
                        colors.append(li.product_id.color_attribute_id)
                    total_model_pairs += li.pairs_count
                for color in colors:
                    (
                        sale,
                        discount,
                        discountpp,
                        referrer,
                        manager,
                        net,
                        cost,
                        difference,
                        margin_percent,
                        pairs_count,
                        factor,
                    ) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
                    lines = self.env["sale.order.line"].search(
                        [
                            ("shoes_campaign_id", "=", record.shoes_campaign_id.id),
                            ("product_tmpl_id", "=", model.id),
                        ]
                    )
                    for li in lines:
                        if li.product_id.color_attribute_id == color:
                            if li.order_id.amount_untaxed != 0:
                                factor = li.price_subtotal / li.order_id.amount_untaxed
                            sale += li.price_subtotal
                            discount += li.price_subtotal * li.discount / 100
                            referrer += li.order_id.commission * factor
                            manager += li.order_id.manager_commission * factor
                            cost += li.product_id.standard_price * li.product_uom_qty
                            pairs_count += li.pairs_count
                        total_pairs += pairs_count
                        net = sale - discount - referrer - manager
                        difference = net - cost
                        if net != 0:
                            margin_percent = difference / net * 100

                    if (sale != 0) or (cost != 0):
                        self.env["shoes.sale.report.line"].create(
                            {
                                "shoes_report_id": record.id,
                                "model_id": model.id,
                                "product_id": li.product_id.id,
                                "color_id": color.id,
                                "sale": sale,
                                "discount": discount,
                                "discount_early_payment": 0,
                                "referrer": referrer,
                                "manager": manager,
                                "total": net,
                                "cost": cost,
                                "margin": difference,
                                "margin_percent": margin_percent,
                                "pairs_count": pairs_count,
                                "total_model_pairs": total_model_pairs,
                            }
                        )
            record["pairs_count"] = total_pairs


# Campos calculados para mostrar en el informe de "Rentabilidad por pedidos":
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_shoes_sale_percent_discount(self):
        for record in self:
            discount = 0
            if record.amount_untaxed != 0:
                discount = (
                                   1 - (record.amount_untaxed / record.amount_undiscounted)
                           ) * 100
            record["global_discount"] = discount

    global_discount = fields.Float(
        string="Discount",
        store=False,
        compute="_get_shoes_sale_percent_discount",
        help="Global discount",
    )

    def _get_shoes_sale_amount_discounted(self):
        for record in self:
            record["amount_discounted"] = (
                    record.amount_undiscounted - record.amount_untaxed
            )

    amount_discounted = fields.Float(
        string="Dis.",
        store=False,
        compute="_get_shoes_sale_amount_discounted",
        help="Discounted amount",
    )

    def _get_shoes_referrer_percent_commission(self):
        for record in self:
            commission = 0
            if (record.amount_untaxed != 0) and (record.commission != 0):
                commission = (
                                     1 - (record.commission * 100 / record.amount_untaxed)
                             ) * 100
            record["referrer_percent_commission"] = commission

    referrer_percent_commission = fields.Float(
        "Com1 %", store=False, compute="_get_shoes_referrer_percent_commission",
        help="Referrer commission percent",
    )

    def _get_shoes_manager_percent_commission(self):
        for record in self:
            commission = 0
            if (record.amount_untaxed != 0) and (record.manager_commission != 0):
                commission = (
                                     1 - (record.manager_commission * 100 / record.amount_untaxed)
                             ) * 100
            record["manager_percent_commission"] = commission

    manager_percent_commission = fields.Float(
        "Com2 %", store=False, compute="_get_shoes_manager_percent_commission",
        help="Manager commission percent",
    )

    def _get_amount_without_commission(self):
        for record in self:
            record["amount_whitout_commission"] = (
                    record.amount_untaxed - record.commission - record.manager_commission
            )

    amount_whitout_commission = fields.Float(
        "Net", store=False, compute="_get_amount_without_commission",
        help="Net amount",
    )

    def _get_cost_before_delivery(self):
        for record in self:
            cost = 0
            for li in record.order_line:
                if (
                        li.product_id.product_tmpl_set_id.id
                        or li.product_id.product_tmpl_single_id.id
                ):
                    cost += li.product_id.standard_price * li.product_uom_qty
            record["cost_before_delivery"] = cost

    cost_before_delivery = fields.Monetary(
        "Cost", store=False, compute="_get_cost_before_delivery",
        help="Cost before delivery",
    )

    def _get_shoes_sale_margin(self):
        for record in self:
            margin = (
                    record.amount_untaxed
                    - record.commission
                    - record.manager_commission
                    - record.cost_before_delivery
            )
            record["shoes_margin"] = margin

    shoes_margin = fields.Monetary(
        "Marg.", store=False, compute="_get_shoes_sale_margin",
        help="Shoes margin",
    )

    def _get_shoes_margin_percent(self):
        for record in self:
            margin = 0
            if record.amount_untaxed != 0:
                margin = (1 - (record.shoes_margin / record.amount_untaxed)) * 100
            record["shoes_margin_percent"] = margin

    shoes_margin_percent = fields.Float(
        "Margin (%)", store=False, compute="_get_shoes_margin_percent"
    )


# Campos calculados para mostrar en el informe de "Rentabilidad por modelos":
class ShoesSaleReportLine(models.Model):
    _name = "shoes.sale.report.line"
    _description = "Shoes Sale Report Line"

    shoes_report_id = fields.Many2one("shoes.sale.report", string="Shoes report")
    model_id = fields.Many2one("product.template", string="Model")
    color_id = fields.Many2one("product.attribute.value", string="Color")
    model_description = fields.Text(
        "Sale description", related="model_id.description_sale"
    )
    sale = fields.Float("Sale", help="Sale amount")
    discount = fields.Float("Disc.", help="Discount amount")
    discount_early_payment = fields.Float("EP", help="Early payment discount")
    referrer = fields.Float("Referrer", help="Referrer commission")
    manager = fields.Float("Manager", help="Manager commission")
    total = fields.Float("Net", help="Net amount")
    cost = fields.Float("Cost", help="Total cost")
    margin = fields.Float("Margin", help="Margin amount")
    margin_percent = fields.Float("Margin %", help="Margin percent")
    pairs_count = fields.Integer("Pairs", help="Pairs count")
    product_id = fields.Many2one("product.product", string="Product", help="Product variant used to related image")
    image = fields.Binary(related="product_id.image_1920", store=False)
    total_model_pairs = fields.Integer("Total model pairs", help="Total pairs by model including all colors and sizes")
