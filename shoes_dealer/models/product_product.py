# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"


    color_attribute_id = fields.Many2one('product.attribute.value', string='Color', store=True)
    size_attribute_id = fields.Many2one('product.attribute.value', string='Size', store=True)
    assortment_attribute_id = fields.Many2one('product.attribute.value', string='Assortment', store=True)


    def update_shoes_pp(self):
        # Chequear si existen las variables de empresa para shoes_dealer, con sus mensajes de alerta:
        self.shoes_dealer_check_environment()

        # Asignar valores de color, talla y surtido directamente en la variante:
        if self.is_pair or self.is_assortment:
            self.set_assortment_color_and_size()

        # Chequear si existen las tallas en el producto par, creándolas (sólo para surtidos):
        if (self.product_tmpl_single_id.id) and (self.is_assortment):
            self.check_for_new_sizes_and_colors()

        # Revisar listas de materiales, si es surtido y ya tiene par asignado:
    #        if (self.product_tmpl_single_id.id) and (self.is_assortment):
    #            self.create_set_bom()



    def shoes_dealer_check_environment(self):
        # Chequear si existen las variables de empresa para shoes_dealer, con sus mensajes de alerta:
        bom_attribute = self.env.user.company_id.bom_attribute_id
        size_attribute = self.env.user.company_id.size_attribute_id
        color_attribute = self.env.user.company_id.color_attribute_id
        prefix = self.env.user.company_id.single_prefix
        if not bom_attribute.id or not size_attribute.id or not color_attribute.id or prefix=="":
            raise UserError(
                "Please set shoes dealer attributes in this company form (Settings => User & companies => Company"
            )

    def set_assortment_color_and_size(self):
        # Asignar valores de color, talla y surtido directamente en la variante:
        for record in self:
            size_attribute = self.env.company.size_attribute_id
            color_attribute = self.env.company.color_attribute_id
            assortment_attribute = self.env.company.bom_attribute_id

            len_size_attribute, len_color_attribute, len_assortment_attribute = 0, 0, 0
            size_value, color_value, assortment_value = False, False, False

            # Caso de una sola variante:
            if len(record.product_tmpl_id.product_variant_ids) == 1:
                size_value, color_value, assortment_value = False, False, False
                for val in record.product_tmpl_id.attribute_line_ids:
                    if val.attribute_id == self.env.company.color_attribute_id:
                        color_value = val.value_ids[0].id
                    if val.attribute_id == self.env.company.size_attribute_id:
                        size_value = val.value_ids[0].id
                    if val.attribute_id == self.env.company.bom_attribute_id:
                        assortment_value = val.value_ids[0].id

            else:
                for li in record.product_template_variant_value_ids:
                    #  Parámetros de empresa:
                    if li.attribute_id.id == size_attribute.id: size_value = li
                    if li.attribute_id.id == color_attribute.id: color_value = li
                    if li.attribute_id.id == assortment_attribute.id: assortment_value = li

                    # Comprobar en PTAL si sólo hay una variante de surtido, color o talla, porque en este caso no se crean product.template.attribute.line:
                    for li in record.product_tmpl_id.attribute_line_ids:
                        if li.attribute_id == size_attribute:
                            size_line = li
                            len_size_attribute = len(li.value_ids.ids)
                        if li.attribute_id == color_attribute:
                            color_line = li
                            len_color_attribute = len(li.value_ids.ids)
                        if li.attribute_id == assortment_attribute:
                            assortment_line = li
                            len_assortment_attribute = len(li.value_ids.ids)

                    # Caso de que haya un un sólo surtido, color o talla en la plantilla, asignación:
                    if len_size_attribute == 1:
                        size_value = size_line.value_ids[0].id
                    if len_color_attribute == 1:
                        color_value = color_line.value_ids[0].id
                    if len_assortment_attribute == 1:
                        assortment_value = assortment_line.value_ids[0].id

                    # Casos de que haya varios surtidos, colores o tallas en la plantilla de producto:
                    if len_size_attribute > 1:
                        # Para buscar la talla:
                        size_value = self.env['product.template.attribute.value'].search([
                            ('product_tmpl_id', '=', record.product_tmpl_id.id),
                            ('id', 'in', record.product_template_variant_value_ids.ids),
                            ('attribute_id', '=', size_attribute.id)
                        ]).product_attribute_value_id.id

                    if len_color_attribute > 1:
                        # Para buscar el color:
                        color_value = self.env['product.template.attribute.value'].search([
                            ('product_tmpl_id', '=', record.product_tmpl_id.id),
                            ('id', 'in', record.product_template_variant_value_ids.ids),
                            ('attribute_id', '=', color_attribute.id)
                        ]).product_attribute_value_id.id

                    if len_assortment_attribute > 1:
                        # Para buscar el surtido:
                        assortment_value = self.env['product.template.attribute.value'].search([
                            ('product_tmpl_id', '=', record.product_tmpl_id.id),
                            ('id', 'in', record.product_template_variant_value_ids.ids),
                            ('attribute_id', '=', assortment_attribute.id)
                        ]).product_attribute_value_id.id

            record.write({'size_attribute_id': size_value,
                          'color_attribute_id': color_value,
                          'assortment_attribute_id': assortment_value,
                          })

    def check_for_new_sizes_and_colors(self):
        # Buscar en PTAL de CHILD el valor de la variante:
        ptal = self.env["product.template.attribute.line"].search(
            [('product_tmpl_id', '=', self.product_tmpl_single_id.id),
             ('attribute_id', '=', self.color_attribute_id.attribute_id.id)])
        # Si no existe, se añade:
        if self.color_attribute_id.id not in ptal.value_ids.ids:
            ptal['value_ids'] = [(4, self.color_attribute_id.id)]
            ptal._update_product_template_attribute_values()

        # Lo mismo para todas las tallas del surtido:
        for li in self.assortment_attribute_id.set_template_id.line_ids:
            size = li.value_id.id
            ptal = self.env["product.template.attribute.line"].search(
                [('product_tmpl_id', '=', self.product_tmpl_single_id.id),
                 ('attribute_id', '=', self.env.company.size_attribute_id.id)])
            # Si no existe, se añade:
            if size not in ptal.value_ids.ids:
                ptal['value_ids'] = [(4, size)]
                ptal._update_product_template_attribute_values()



    def create_set_bom(self):
        # Crear lista de materiales, si es surtido y ya tiene par asignado:
        for record in self:
            pt_single = record.product_tmpl_single_id
            set_template = record.assortment_attribute_id.set_template_id
            color_value = record.color_attribute_id

            # Limpieza de BOMS huérfanas:
            bomsdelete = self.env['mrp.bom'].search([('is_assortment', '=', True), ('product_id', '=', False)]).unlink()

            if pt_single.id and record.is_assortment and not record.variant_bom_ids:
                # Creación de LDM:
                code = (
                        record.name
                        + " // "
                        + str(set_template.code)
                        + " "
                        + str(color_value.name)
                )

                bom = self.env["mrp.bom"].create(
                    {
                        "code": code,
                        "type": "normal",
                        "product_qty": 1,
                        "product_tmpl_id": record.product_tmpl_id.id,
                        "product_id": record.id,
                    }
                )

                # Creación de líneas en LDM para cada talla del surtido:
                for li in set_template.line_ids:
                    # El producto "single (o par)" con estos atributos, que se usará en la LDM:
                    pp_size = self.env['product.product'].search([
                        ('product_tmpl_id', '=', record.product_tmpl_single_id.id),
                        ('color_attribute_id', '=', record.color_attribute_id.id),
                        ('size_attribute_id', '=', li.value_id.id)])

                    # Creación de las líneas de la LDM:
                    new_bom_line = self.env["mrp.bom.line"].create(
                        {
                            "bom_id": bom.id,
                            "product_id": pp_size.id,
                            "product_qty": li.quantity,
                        }
                    )


                # Actualizar campo base_unit_count del estándar para que muestre precio unitario en website_sale,
                # si fuera un par sólo, la cantidad a indicar es 0 para que no se muestre, por esta razón seguimos
                # manteniendo el campo del desarrollo paris_count en los distintos modelos:
                # 2º actualizamos el precio de venta del surtido al crear:
                base_unit_count = 0
                for bom_line in bom.bom_line_ids:
                    base_unit_count += bom_line.product_qty
                if base_unit_count == 1:
                    base_unit_count = 0
                record.write({"base_unit_count": base_unit_count})



    # Pares por variante de producto, se usará en el cálculo de tarifas y líneas de venta:
    def _get_shoes_product_product_pair_count(self):
        for record in self:
            count = 1
            bom = self.env['mrp.bom'].search([('product_id','=',record.id)])
            if bom.ids:
                count = bom[0].pairs_count
            record['pairs_count'] = count
    pairs_count = fields.Integer('Pairs', store=False, compute='_get_shoes_product_product_pair_count')



    # Product assortment (to be printed on sale.order and account.move reports):
    # 2024/02 REVISAR ESTO, POSIBLEMENTE SE PUEDE CAMBIAR POR UN RELATED DE assortment_attribute_id.set_template_id.code
    def _get_product_assortment_code(self):
        for record in self:
            assortment_code = ""
            assortment_attribute = self.env.user.company_id.bom_attribute_id

            # El campo en el product.product es product_template_variant_value_ids
            # Este campo es un m2m a product.template.attribute.value
            # Dentro de ese modelo hay un attribute_id que apunta a product_attribute (que ha de ser el de la compañía) y
            # un product_attribute_value_id que apunta a product.attribute.value

            # Si hay varios atributos sería lo siguiente:
            if record.product_template_variant_value_ids.ids:
                ptvv = self.env['product.template.attribute.value'].search(
                    [('id', 'in', record.product_template_variant_value_ids.ids),
                     ('attribute_id', '=', assortment_attribute.id)])
            # Para el caso de una sóla variante en el template el valor del campo es False:
            else:
                ptvv = self.env['product.template.attribute.value'].search(
                    [('product_tmpl_id', '=', record.product_tmpl_id.id),
                     ('attribute_id', '=', assortment_attribute.id)])

            # este modelo tiene un campo que es "set_template_id" que apunta al modelo "set.template"
            # Los valores que nos interesan son las líneas de este último, pero utilizamos el campo code para impresión)
            if ptvv.id:
                assortment_code = ptvv.product_attribute_value_id.set_template_id.code
            record['assortment_code'] = assortment_code
    assortment_code = fields.Char('Assortment', store=False, compute='_get_product_assortment_code')

