# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = [
        "product.template",
        "website.seo.metadata",
        "website.published.multi.mixin",
        "website.searchable.mixin",
        "rating.mixin",
    ]
    _name = "product.template"
    _mail_post_access = "read"
    _check_company_auto = True

    shoes_campaign_id = fields.Many2one(
        "project.project", string="Campaign", store=True, copy=True, tracking=10
    )
    gender = fields.Selection(
        [("man", "Man"), ("woman", "Woman"), ("unisex", "Unisex")],
        string="Serial",
        copy=True,
        store=True,
    )

    @api.depends('attribute_line_ids.value_ids')
    def _get_shoes_product_update_required(self):
        for record in self:
            valueids = ""
            for at in record.attribute_line_ids:
                for va in at.value_ids:
                    valueids += str(va.id)
        record['valueids'] = valueids
    valueids = fields.Char('Value IDS', store=True,
                           compute='_get_shoes_product_update_required',
                           help='Internal field used to update product variants attributes and BOM from AA')
    @api.depends("attribute_line_ids")
    def _get_is_assortment(self):
        is_assortment, color, assortment = False, False, False
        color_attribute = self.env.company.color_attribute_id
        assortment_attribute = self.env.company.bom_attribute_id
        for li in self.attribute_line_ids:
            if li.attribute_id == color_attribute:
                color = True
            if li.attribute_id == assortment_attribute:
                assortment = True
        if color and assortment:
            is_assortment = True
        self.is_assortment = is_assortment

    is_assortment = fields.Boolean(
        "Is Assortment", store=True, compute="_get_is_assortment"
    )

    @api.depends("attribute_line_ids")
    def _get_is_pair(self):
        is_pair, color, size = False, False, False
        color_attribute = self.env.company.color_attribute_id
        size_attribute = self.env.company.size_attribute_id
        for li in self.attribute_line_ids:
            if li.attribute_id == color_attribute:
                color = True
            if li.attribute_id == size_attribute:
                size = True
        if color and size:
            is_pair = True
        self.is_pair = is_pair

    is_pair = fields.Boolean("Is Pair", store=True, compute="_get_is_pair")

    material_id = fields.Many2one(
        "product.material", string="Material", store=True, copy=True
    )
    manufacturer_id = fields.Many2one(
        "res.partner", string="Manufacturer", store=True, copy=True
    )

    # Plantilla de producto "surtido" que genera los "pares":
    product_tmpl_set_id = fields.Many2one(
        "product.template", string="Parent", store=True, copy=False
    )

    # Plantilla de producto "pares" generada desde el "surtido":
    product_tmpl_single_id = fields.Many2one(
        "product.template", string="Child", store=True, copy=False
    )
    product_tmpl_single_list_price = fields.Float(
        "Precio del par", related="product_tmpl_single_id.list_price"
    )

    # Plantilla de producto para relacionar surtidos y pares con el modelo para informes (independiente de talla):
    @api.depends("product_tmpl_single_id", "product_tmpl_set_id")
    def _get_pt_shoes_model(self):
        for record in self:
            model = False
            if record.product_tmpl_single_id.id:
                model = record.product_tmpl_single_id.id
            if record.product_tmpl_set_id.id:
                model = record.id
            record["product_tmpl_model_id"] = model

    product_tmpl_model_id = fields.Many2one(
        "product.template", string="Model", store=True, compute="_get_pt_shoes_model"
    )

    # El precio de coste es la suma de Exwork + portes, si existe el par se mostrará uno u otro campo:
    exwork_currency_id = fields.Many2one(
        "res.currency",
        store=False,
        related='manufacturer_id.property_purchase_currency_id'
# Modificado 02/24 para usar la moneda de cada fabricante en vez de la genérica de empresa.:
#        default=lambda self: self.env.user.company_id.exwork_currency_id,
    )
    exwork = fields.Monetary("Exwork", store=True, copy=True, tracking="10")
    exwork_single = fields.Monetary(
        "Exwork single",
        store=True,
        copy=True,
        tracking="10",
        related="product_tmpl_single_id.exwork",
        readonly=False,
    )
    shipping_price = fields.Monetary(
        "Shipping price", store=True, copy=True, tracking="10"
    )
    shipping_single_price = fields.Monetary(
        "Shipping single price",
        store=True,
        copy=True,
        tracking="10",
        related="product_tmpl_single_id.shipping_price",
        readonly=False,
    )
    campaign_code = fields.Char("Campaign Code", store=True, copy=False)

    # Product colors from product.template.attribute.line (to be printed on labels):
    def _get_product_colors(self):
        for record in self:
            colors = []
            color_attribute = self.env.user.company_id.color_attribute_id

            # El campo en el product.template es attribute_line_ids
            # Este campo es un o2m a product.template.attribute.line, que tiene product_tmpl_id y attribute_id
            # attribute_id que apunta a product_attribute (que ha de ser el de la compañía) y
            # un value_ids que apunta a directamente a product.attribute.value

            if record.attribute_line_ids.ids:
                ptal = self.env["product.template.attribute.line"].search(
                    [
                        ("product_tmpl_id", "=", record.id),
                        ("attribute_id", "=", color_attribute.id),
                    ]
                )
                if ptal.id:
                    colors = ptal.value_ids.ids
            record["pt_colors_ids"] = [(6, 0, colors)]

    pt_colors_ids = fields.Many2many(
        "product.attribute.value",
        "Product colors",
        store=False,
        compute="_get_product_colors",
    )

    # Actualizar el precio de los surtidos cuando cambia el precio del par:
    @api.onchange("list_price")
    def update_set_price_by_pairs(self):
        for record in self:
            if record.product_tmpl_set_id.id:
                for pp in record.product_tmpl_set_id.product_variant_ids:
                    pp.write({"lst_price": record.list_price * pp.pairs_count})
            # Esta parte funcionará al ser llamada desde la creación de pares:
            if record.product_tmpl_single_id.id:
                for pp in record.product_variant_ids:
                    pp.write({"lst_price": record.list_price * pp.pairs_count})

    # Cuando se actualicen los atributos de PT, que lo hagan los PP:
    @api.onchange('valueids')
    def update_shoes_variants(self):
        # Chequear si existen las variables de empresa para shoes_dealer, con sus mensajes de alerta:
        bom_attribute = self.env.user.company_id.bom_attribute_id
        size_attribute = self.env.user.company_id.size_attribute_id
        color_attribute = self.env.user.company_id.color_attribute_id
        prefix = self.env.user.company_id.single_prefix
        if not bom_attribute.id or not size_attribute.id or not color_attribute.id or prefix == "":
            raise UserError(
                "Please set shoes dealer attributes in this company form (Settings => User & companies => Company"
            )

        for record in self:
            # Actualizar variantes:
            for pp in record.product_variant_ids:
                # Asignar valores de color, talla y surtido directamente en la variante:
                if pp.is_pair or pp.is_assortment:
                    pp.set_assortment_color_and_size()
                # Chequear si existen las tallas en el producto par y listas de materiales (sólo para surtidos):
                if (pp.product_tmpl_single_id.id) and (pp.is_assortment):
                    pp.check_for_new_sizes_and_colors()
                    pp.create_set_bom()

            for pp in record.product_tmpl_single_id.product_variant_ids:
                # Asignar valores de color, talla y surtido directamente en la variante:
                if pp.is_pair or pp.is_assortment:
                    pp.set_assortment_color_and_size()
























    def create_shoe_pairs(self):
        for record in self:
            if not record.shoes_campaign_id.id:
                raise UserError("Assign a campaign before pairs creation !!")
            record.create_single_products()
            # REVISAR, TIENE AA:
            record.update_standard_price_on_variants()
            # REVISAR, FÁCIL LLEVAR A PP:
            record.update_product_template_campaign_code()
            # REVISAR, TIENE UN DEPENDS:
            record.update_set_price_by_pairs()

    def create_single_products(self):
        # Nueva versión desde variantes desde atributo:
        for record in self:
            # 1. Chequeo variante parametrizada de empresa y producto, con sus mensajes de alerta:
            bom_attribute = self.env.user.company_id.bom_attribute_id
            size_attribute = self.env.user.company_id.size_attribute_id
            color_attribute = self.env.user.company_id.color_attribute_id
            prefix = self.env.user.company_id.single_prefix
            single_sale = self.env.user.company_id.single_sale
            single_purchase = self.env.user.company_id.single_purchase

            if not bom_attribute.id or not size_attribute.id:
                raise UserError(
                    "Please set shoes dealer attributes in this company form (Settings => User & companies => Company"
                )

            # CREACIÓN DEL PRODUCTO PAR, SI NO EXISTE:
            if not record.product_tmpl_single_id.id:
                colors, sizes, campaign_code = [], [], ""
                if record.campaign_code:
                    campaign_code = "P" + record.campaign_code
                # Cálculo de precio de coste con cambio de moneda:
                standard_price = record.standard_price
                if (
                    (record.shoes_campaign_id.id)
                    and (record.shoes_campaign_id.currency_exchange)
                    and (record.exwork)
                ):
                    standard_price = (
                        record.exwork * record.shoes_campaign_id.currency_exchange
                    )

                newpt = self.env["product.template"].create(
                    {
                        "name": str(prefix) + record.name,
                        "product_tmpl_set_id": record.id,
                        "shoes_campaign_id": record.shoes_campaign_id.id,
                        "list_price": record.list_price,
                        "standard_price": record.standard_price,
                        "exwork": record.exwork,
                        "shipping_price": record.shipping_price,
                        "sale_ok": single_sale,
                        "purchase_ok": single_purchase,
                        "detailed_type": "product",
                        "categ_id": record.categ_id.id,
                        "product_brand_id": record.product_brand_id.id,
                        "campaign_code": campaign_code,
                    }
                )
                record.write({"product_tmpl_single_id": newpt.id})

                for li in record.attribute_line_ids:
                    if li.attribute_id.id == bom_attribute.id:
                        for ptav in li.value_ids:
                            for set_line in ptav.set_template_id.line_ids:
                                if set_line.value_id.id not in sizes:
                                    sizes.append(set_line.value_id.id)
                        new_ptal = self.env["product.template.attribute.line"].create(
                            {
                                "product_tmpl_id": newpt.id,
                                "attribute_id": size_attribute.id,
                                "value_ids": [(6, 0, sizes)],
                            }
                        )
                        new_ptal._update_product_template_attribute_values()

                    elif li.attribute_id.id == color_attribute.id:
                        for ptav in li.value_ids:
                            if ptav.id not in colors:
                                colors.append(ptav.id)
                        new_ptal = self.env["product.template.attribute.line"].create(
                            {
                                "product_tmpl_id": newpt.id,
                                "attribute_id": color_attribute.id,
                                "value_ids": [(6, 0, colors)],
                            }
                        )
                        new_ptal._update_product_template_attribute_values()

    # 2024.02 Esto ya no haría falta desde PT si funciona la AA de PP.
    def update_color_and_size_attributes(self):
        for record in self:
            for pp in record.product_variant_ids:
                pp.set_assortment_color_and_size()
            for pp in record.product_tmpl_single_id.product_variant_ids:
                pp.set_assortment_color_and_size()

    # Actualizar precios de coste, en base al exwork y cambio de moneda (NO FUNCIONA ONCHANGE => AA):
    # @api.onchange('exwork', 'exwork_single', 'product_variant_ids', 'campaing_id')
    def update_standard_price_on_variants(self):
        # Caso de actualizar el precio desde el PAR:
        for record in self:
            if record.product_tmpl_set_id.id:
                standard_price = (
                    record.exwork * record.shoes_campaign_id.currency_exchange
                )
                for pp in record.product_variant_ids:
                    pp.write({"standard_price": standard_price})
                for pp in record.product_tmpl_set_id.product_variant_ids:
                    pp.write({"standard_price": standard_price * pp.pairs_count})
            # Caso de actualizarse el precio desde el SURTIDO:
            if record.product_tmpl_single_id.id:
                standard_price = (
                    record.product_tmpl_single_id.exwork
                    * record.shoes_campaign_id.currency_exchange
                )
                for pp in record.product_variant_ids:
                    pp.write({"standard_price": standard_price * pp.pairs_count})
                for pp in record.product_tmpl_single_id.product_variant_ids:
                    pp.write({"standard_price": standard_price})

    def update_product_template_campaign_code(self):
        # default_code no vale porque se requite cada año y no está disponible en PT si hay variantes.
        for record in self:
            if not record.shoes_campaign_id.id:
                raise UserError("Please, assign campaign prior to create codes !!")
            if not record.campaign_code:
                code = str(record.shoes_campaign_id.campaign_code) + "."
                # Caso de actualizar desde el PAR (código "Pxx.")
                if record.product_tmpl_set_id.id:
                    record.write({"campaign_code": "P" + code})
                    record.product_tmpl_set_id.write({"campaign_code": code})
                # Caso de actualizarse el precio desde el SURTIDO:
                if record.product_tmpl_single_id.id:
                    record.write({"campaign_code": code})
                    record.product_tmpl_single_id.write({"campaign_code": "P" + code})
                next_code = record.shoes_campaign_id.campaign_code + 1
                record.shoes_campaign_id.write({"campaign_code": next_code})

    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(["name", "default_code", "campaign_code"])
        return [
            (
                template.id,
                "%s%s%s"
                % (
                    template.default_code and "[%s] " % template.default_code or "",
                    template.name,
                    template.campaign_code and " [%s] " % template.campaign_code or "",
                ),
            )
            for template in self
        ]

    def update_supplier_info(self):
        for product in self:
            if not product.manufacturer_id.id:
                raise UserError(
                    "Asigna el fabricante para poder actualizar la tarifa de proveedor."
                    + ": "
                    + product.name
                )
            product.variant_seller_ids.unlink()
            for variant in product.product_variant_ids:
                price = product.exwork_single
                if product.product_tmpl_single_id.id:
                    price = product.exwork_single * variant.pairs_count
                list_price = self.env["product.supplierinfo"].create(
                    {
                        "partner_id": product.manufacturer_id.id,
                        "min_qty": "1",
                        "price": price,
                        "product_id": variant.id,
                        "currency_id": product.exwork_currency_id.id,
                        "product_tmpl_id": product.id,
                    }
                )

    # Notas del desarrollo:
    # =====================
    # product template genera PRODUCT.PRODUCT en: product_variant_ids
    # Cada variante tiene unos valores de sus variantes en:
    #   Campo: product_template_variant_value_ids
    #   Modelo: product.template.attribute.value
    # El modelo product.template.attribute.value es una línea:
    #   attribute_line_id (mo2) a product.template.attribute.line
    #   m2o relacionado por el anterior: attribute_id
    #   product_attribute_value_id (m2o) a product.attribute.value
    #   name (char) related: product_attribute_value_id.name
    # Modelo product.attribute.value:
    #   attribute_id (m2o a product.attribute)
    #   set_template_id (m2o) a set.template
    # Model set.template:
    #   name + code (mandatories)
    #   line_ids (o2m) set.template.line (value_id, quantity)
