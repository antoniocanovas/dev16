# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

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

    @api.depends('create_date')
    def get_product_color(self):
        for record in self:
            color_attribute = self.env.company.color_attribute_id

            # Para buscar el color:
            color_value = self.env['product.template.attribute.value'].search([
                ('product_tmpl_id', '=', record.product_tmpl_id.id),
                ('id', 'in', record.product_template_variant_value_ids.ids),
                ('attribute_id', '=', color_attribute.id)]).product_attribute_value_id.id

            # Caso de que sólo haya un COLOR, no existe el registro anterior PTAV, buscamos en la línea atributo de PT:
            if not color_value:
                self.ensure_one()
                color_value = self.env['product.template.attribute.line'].search([
                    ('product_tmpl_id', '=', record.product_tmpl_id.id),
                    ('attribute_id', '=', color_attribute.id)]).product_template_value_ids.product_attribute_value_id.id
            if not color_value: color_value = 0
            record['color_attribute_id'] = color_value
    color_attribute_id = fields.Many2one('product.attribute.value', string='Color', store=True, compute='get_product_color')

#    @api.depends('create_date')
    def get_product_size(self):
        for record in self:
            size_attribute = self.env.company.size_attribute_id

            # Para buscar la talla:
            size_value = self.env['product.template.attribute.value'].search([
                ('product_tmpl_id', '=', record.product_tmpl_id.id),
                ('id', 'in', record.product_template_variant_value_ids.ids),
                ('attribute_id', '=', size_attribute.id)]).product_attribute_value_id.id

            # Caso de que sólo haya un COLOR, no existe el registro anterior PTAV, buscamos en la línea atributo de PT:
            if not size_value:
                self.ensure_one()
                size_value = self.env['product.template.attribute.line'].search([
                    ('product_tmpl_id', '=', record.product_tmpl_id.id),
                    ('id', 'in', record.product_template_variant_value_ids.ids),
                    ('attribute_id', '=', size_attribute.id)]).product_template_value_ids.product_attribute_value_id.id

            if not size_value: size_value = 0
#            record['size_attribute_id'] = size_value
#    size_attribute_id = fields.Many2one('product.attribute.value', string='Size', store=True, compute='get_product_size')