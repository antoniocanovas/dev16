# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # Pares por variante de producto, se usará en el cálculo de tarifas y líneas de venta:
    @api.depends('bom_line_ids','bom_line_ids.product_qty')
    def _get_shoes_bom_pair_count(self):
        for record in self:
            count = 0
            if record.bom_line_ids.ids:
                for li in record.bom_line_ids:
                    count += li.product_qty
            else: count = 1
            record['pairs_count'] = count
    pairs_count = fields.Integer('Pairs', store=True, compute='_get_shoes_bom_pair_count')

    set_pairs_count = fields.Integer('Set pairs',
                                     related='product_id.assortment_attribute_id.set_template_id.pairs_count')

    def _create_assortment_bom_lines(self):
        for record in self:
            # Creación de líneas en LDM para cada surtido:
            set_template = record.product_id.assortment_attribute_id.set_template_id
            product = record.product_id
                # Para surtidos sin líneas:
            if (record.product_id.is_assortment) and not (record.bom_line_ids.ids):
                color_value = record.product_id.color_attribute_id

                for li in set_template.line_ids:
                    size_value = li.value_id
                    size_quantity = li.quantity

                    # El producto "single (o par)" con estos atributos, que se usará en la LDM:
                    pp_single = self.env["product.product"].search([
                        ('product_tmpl_id', '=', record.product_id.product_tmpl_single_id.id),
                        ('size_attribute_id', '=', size_value.id),
                        ('color_attribute_id', '=', color_value.id)
                    ])

                    # Creación de las líneas de la LDM:
                    new_bom_line = self.env["mrp.bom.line"].create(
                        {
                            "bom_id": record.id,
                            "product_id": pp_single.id,
                            "product_qty": size_quantity,
                        }
                    )

                # Actualizar campo base_unit_count del estándar para que muestre precio unitario en website_sale,
                # si fuera un par sólo, la cantidad a indicar es 0 para que no se muestre, por esta razón seguimos
                # manteniendo el campo del desarrollo paris_count en los distintos modelos:
                # 2º actualizamos el precio de venta del surtido al crear:
                base_unit_count = 0
                for bom_line in record.bom_line_ids:
                    base_unit_count += bom_line.product_qty
                if base_unit_count == 1:
                    base_unit_count = 0
                product.write({"base_unit_count": base_unit_count})