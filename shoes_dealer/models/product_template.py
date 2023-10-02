# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    #    Ya no hace falta porque los productos "single" se generan desde las variantes:
    #    set_code = fields.Char('Code', store=True, copy=False)
    #    set_template_ids = fields.Many2many('set.template', string='Set templates', store="True",)

    # Plantilla de producto "surtido" que general los "pares":
    product_tmpl_set_id = fields.Many2one('product.template', string='Parent', store=True)
    def _get_hide_set(self):
        hide = True
        bom_attribute = self.env.user.company_id.bom_attribute_id
        for li in self.attribute_line_ids:
            if li.attribute_id.id == bom_attribute.id:
                hide=False
        self.product_tmpl_set_hide = hide
    product_tmpl_set_hide = fields.Boolean('Hide set', store=False, compute='_get_hide_set')



    # Plantilla de producto "pares" generada desde el "surtido":
    product_tmpl_single_id  = fields.Many2one('product.template', string='Child', store=True)
    def _get_single_hide(self):
        hide = True
        size_attribute = self.env.user.company_id.bom_attribute_id
        for li in self.attribute_line_ids:
            if li.attribute_id.id == size_attribute.id:
                hide=False
        self.product_tmpl_single_hide = hide
    product_tmpl_single_hide = fields.Boolean('Hide set', store=False, compute='_get_single_hide')

    # De momento no sé si pondré este o2m:
    #    set_product_ids  = fields.One2many('product.template','parent_id', string='Set products', store=True, readonly=True)


    def create_single_products(self):
        # Nueva versión desde variantes desde atributo:
        for record in self:
            # 1. Chequeo variante parametrizada de empresa y producto, con sus mensajes de alerta:
            bom_attribute = self.env.user.company_id.bom_attribute_id
            size_attribute = self.env.user.company_id.size_attribute_id
            color_attribute = self.env.user.company_id.color_attribute_id
            prefix = self.env.user.company_id.single_prefix
            pt_single = record.product_tmpl_single_id

            if not bom_attribute.id or not size_attribute.id:
                raise UserError('Please set shoes dealer attributes in this company form (Settings => User & companies => Company')
            if not pt_single.id:
                raise UserError('Please create firt the single product name, I will create variants later reading Sets')
            if not record.product_tmpl_single_id.id:
                raise UserError('Crea el producto unitario para poder usarlo en la lista de pares del surtido.')

            # CREACIÓN DEL PRODUCTO PAR, SI NO EXISTE:
            if not record.product_tmpl_single_id.id:
                colors, sizes = [], []
                newpt = self.env['product.template'].create({'name': str(prefix) + record.name,
                                                             'product_tmpl_set_id':record.id})
                record.write({'product_tmpl_single_id': newpt.id})

                for li in record.attribute_line_ids:
                    if (li.attribute_id.id == bom_attribute.id):
                        for ptav in li.value_ids:
                            for set_line in ptav.set_template_id.line_ids:
                                if set_line.value_id.id not in sizes: sizes.append(set_line.value_id.id)
                        new_ptal = self.env['product.template.attribute.line'].create(
                            {'product_tmpl_id': newpt.id, 'attribute_id': size_attribute.id,
                             'value_ids': [(6, 0, sizes)]})

                    elif (li.attribute_id.id == color_attribute.id):
                        for ptav in li.value_ids:
                            if ptav.id not in colors: colors.append(ptav.id)
                        new_ptal = self.env['product.template.attribute.line'].create(
                            {'product_tmpl_id': newpt.id, 'attribute_id': color_attribute.id,
                             'value_ids': [(6, 0, colors)]})
            # ------ FIN CREACIÓN PRODUCTO "PAR"

            # Variantes de surtido y color, creación de listas de materiales con los pares de la plantilla:
            for pr in record.product_variant_ids:
                # Buscar en atributos el de surtido y apuntar a su plantilla, para después tomar las cantidades para la LDM:
                set_template = self.env['product.template.attribute.value'].search([
                    ('product_tmpl_id', '=', record.id),
                    ('id', 'in', pr.product_template_variant_value_ids.ids),
                    ('attribute_id', '=', bom_attribute.id)]).product_attribute_value_id.set_template_id

                # Lo mismo para buscar el color:
                color_value = self.env['product.template.attribute.value'].search([
                    ('product_tmpl_id', '=', record.id),
                    ('id', 'in', pr.product_template_variant_value_ids.ids),
                    ('attribute_id', '=', color_attribute.id)]).product_attribute_value_id

                # Como hay surtido, continuamos:
                if set_template.id:
                    # Creación de LDM por surtido:
                    code = pr.name + " // " + str(set_template.code) + " " + str(set_template.name)
                    pr_set_bom = self.env['mrp.bom'].search([('product_id', '=', pr.id)])

                    if not pr_set_bom.ids:
                        exist = self.env['mrp.bom'].create({'code': code, 'type': 'normal', 'product_qty': 1,
                                                            'product_tmpl_id': record.id, 'product_id': pr.id})
                    else:
                        exist = pr.bom_ids[0]
                        exist.bom_line_ids.unlink()

                    # Creación de líneas en LDM para cada talla del surtido:
                    for li in set.line_ids:
                        size_value = li.value_id
                        size_quantity = li.quantity

                    # Creación de líneas en LDM para cada talla del surtido:
                    for li in set.line_ids:
                        size_value = li.value_id
                        size_quantity = li.quantity

                        # Buscar línea de valor para el PT de single y esta talla, que después se usará en el "pp single" (de momento sólo 1 attrib por proucto):
                        ptav_size = self.env['product.template.attribute.value'].search(
                            [('attribute_id', '=', size_attribute.id),
                             ('product_attribute_value_id', '=', size_value.id),
                             ('product_tmpl_id', '=', pt_single.id)])
                        ptav_color = self.env['product.template.attribute.value'].search(
                            [('attribute_id', '=', color_attribute.id),
                             ('product_attribute_value_id', '=', color_value.id),
                             ('product_tmpl_id', '=', pt_single.id)])

                        # El producto "single (o par)" con estos atributos, que se usará en la LDM:
                        pp_single = self.env['product.product'].search(
                            [('product_template_variant_value_ids', 'in', ptav_size.id),
                             ('product_template_variant_value_ids', 'in', ptav_color.id)])
                        if not pp_single.ids: raise UserError('No encuentro esa talla y color en el producto PAR')

                        # Creación de las líneas de la LDM:
                        new_bom_line = self.env['mrp.bom.line'].create({'bom_id': exist.id,
                                                                   'product_id': pp_single.id,
                                                                   'product_qty': size_quantity,
                                                                   })

    # Notas del desarrollo:
    # =====================
    # product template genera variantes en: product_variant_ids
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