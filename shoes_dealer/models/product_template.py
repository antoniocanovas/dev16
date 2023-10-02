# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    #       Ya no hace falta porque los productos "single" se generan desde las variantes:
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
            bom_attribute = env.user.company_id.bom_attribute_id
            size_attribute = env.user.company_id.size_attribute_id
            color_attribute = env.user.company_id.color_attribute_id
            pt_single = record.product_tmpl_single_id

            if not bom_attribute.id or not size_attribute.id:
                raise UserError('Please set shoes dealer attributes in this company form (Settings => User & companies => Company')
            if not pt_single.id:
                raise UserError('Please create firt the single product name, I will create variants later reading Sets')
            if not record.product_tmpl_single_id.id:
                raise UserError('Crea el producto unitario para poder usarlo en la lista de pares del surtido.')

            # Pasar por todas las variantes para crear sus listas de materiales con los pares del surtido:
            for pr in record.product_variant_ids:
                # Buscar atributo de surtido y plantilla de surtido para después tomar las cantidades para la LDM:
                set_value = env['product.template.attribute.value'].\
                    search([('product_tmpl_id', '=', record.id),
                            ('id', 'in',pr.product_template_variant_value_ids.ids),
                            ('attribute_id', '=',bom_attribute.id)]).product_attribute_value_id
                set = set_value.set_template_id

                if set.id:
                    size_value = li.value_id.name
                    size_quantity = li.quantity

                    for li in set.line_ids:
                        size_value = li.value_id.name
                        color_value = li.value_id.name
                        size_quantity = li.quantity

                        # Buscar línea de valor para el PT de single y esta talla, que después se usará en el "pp single" (de momento sólo 1 attrib por proucto):
                        ptav_size = self.env['product.template.attribute.value'].search(
                            [('attribute_id', '=', size_attribute.id), ('name', '=', size_value),
                             ('product_tmpl_id','=',pt_single_id.id)])
                        ptav_color = self.env['product.template.attribute.value'].search(
                            [('attribute_id', '=', color_attribute.id), ('name', '=', color_value),
                             ('product_tmpl_id','=',pt_single_id.id)])

                        pp_single = env['product.product'].search(
                            [('product_template_variant_value_ids', 'in', ptav_size.id),
                             ('product_template_variant_value_ids', 'in', ptav_color.id)])




                        # VOY POR AQUÍ:
                        linea_variantes = env['product.template.attribute.value'].search(
                            [('product_tmpl_id', '=', record.product_tmpl_single_id.id)])
                        raise UserError(linea_variantes)

                        exist = self.env['product.product'].search([('product_tmpl_id','=',pt_single.id)])

                        if not exist.bom_ids.ids:
                            new_bom = self.env['mrp.bom'].create({'code': code, 'type': 'normal', 'product_qty': 1,
                                                                  'product_tmpl_id': exist.id, })
                        # Mismo chequeo con las líneas bom:
                        if not (exist.bom_ids.bom_line_ids.ids):
                            # Crear las líneas del BOM tras haber buscado si existen las variantes en SELF:
                            for va in te.line_ids:
                                # Búsqueda de línea de valor de atributo variable para cada talla de producto en SURTIDO:
                                ptav2 = self.env['product.template.attribute.value'].search(
                                    [('product_tmpl_id', '=', self.id), ('product_attribute_value_id', '=', va.value_id.id)])
                                # Búsqueda de producto con ambos valores de atributo (principal y variable):
                                exist_pp = self.env['product.product'].search([('product_tmpl_id', '=', self.id),
                                                                               ('product_template_variant_value_ids', 'in',
                                                                                ptav1.id),
                                                                               ('product_template_variant_value_ids', 'in',
                                                                                ptav2.id)])
                                # Creación de línea de BOM, o ERROR de que la variante (talla) no existe:
                                if exist_pp.id:
                                    new_bom_line = self.env['mrp.bom.line'].create({'bom_id': new_bom.id,
                                                                                    'product_id': exist_pp.id,
                                                                                    'product_qty': va.quantity,
                                                                                    })
                                else:
                                    raise UserError("No existe: " + va.name)
                                    # jugar con value_id y quantity, o con el nombre que es un diccionario.
                        # 1. Crear la lista de materiales si no existe.
                        # 2. Buscar el pp_single relacionado para cada valor y rellenar el BOM.
