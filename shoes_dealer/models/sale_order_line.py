# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    referrer_id = fields.Many2one(
        "res.partner", related="order_id.referrer_id", store=True
    )

    # Comercialmente en cada pedido quieren saber cuántos pares se han vendido:
    @api.depends("product_id", "product_uom_qty")
    def _get_shoes_sale_line_pair_count(self):
        for record in self:
            record["pairs_count"] = (
                record.product_id.pairs_count * record.product_uom_qty
            )

    pairs_count = fields.Integer(
        "Pairs", store=True, compute="_get_shoes_sale_line_pair_count"
    )

    # Precio especial del para en la línea de ventas, recalculará precio unitario del producto surtido:
    special_pair_price = fields.Monetary("SPP", help="Special pair price")

    @api.onchange("special_pair_price")
    def _update_price_unit_from_spp(self):
        for record in self:
            record["price_unit"] = (
                record.pairs_count * record.special_pair_price / record.product_uom_qty
            )

    # Para informes:
    state_id = fields.Many2one(
        "res.country.state",
        "Customer State",
        readonly=True,
        store=True,
        related="order_partner_id.state_id",
    )

    country_id = fields.Many2one(
        "res.country",
        "Customer Country",
        readonly=True,
        store=True,
        related="order_partner_id.country_id",
    )

    product_tmpl_model_id = fields.Many2one(
        "product.template",
        string="Shoes Model",
        store=True,
        related="product_id.product_tmpl_model_id",
    )
    color_attribute_id = fields.Many2one(
        "product.attribute.value",
        string="Shoes Color",
        store=True,
        related="product_id.color_attribute_id",
    )
    shoes_campaign_id = fields.Many2one(
        "project.project",
        string="Shoes Campaign",
        store=True,
        related="order_id.shoes_campaign_id",
    )
    product_brand_id = fields.Many2one(
        "product.brand",
        string="Brand",
        store=True,
        related="product_id.product_brand_id",
    )
    product_tmpl_id = fields.Many2one(
        string="S Model",
        comodel_name="product.template",
        related="product_id.product_tmpl_id",
        store=True,
        help="Used for group views in sale order line",
    )
    manufacturer_id = fields.Many2one(
        string="Manufacturer",
        comodel_name="res.partner",
        related="product_id.manufacturer_id",
        store=True,
        help="Used for group by manufacturer in sale order line views",
    )

    @api.depends("state")
    def _get_quoted_quantity(self):
        for record in self:
            total = 0
            if record.state not in ["sale", "done", "cancel"]:
                total = record.product_uom_qty
            record["qty_quoted"] = total

    qty_quoted = fields.Float(
        "Quoted qty", store=True, copy=False, compute="_get_quoted_quantity"
    )

    # ========= FIN INFORMES

    # Precio por par según tarifa:
    @api.depends("product_id", "price_unit")
    def _get_shoes_pair_price(self):
        for record in self:
            total = 0
            if record.pairs_count != 0:
                total = record.price_subtotal / record.pairs_count
            record["pair_price"] = total

    pair_price = fields.Float("Pair price", store=True, compute="_get_shoes_pair_price")

    product_saleko_id = fields.Many2one(
        "product.product", string="Product KO", store=True, copy=True
    )

    @api.onchange("product_saleko_id")
    def change_saleproductok_2_saleproductko(self):
        self.product_id = self.product_saleko_id.id
