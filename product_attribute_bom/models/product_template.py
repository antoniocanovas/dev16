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
    # Plantilla de producto "pares" generada desde el "surtido":
    product_tmpl_single_id  = fields.Many2one('product.template', string='Child', store=True)

    # De momento no sé si pondré este o2m:
    #    set_product_ids  = fields.One2many('product.template','parent_id', string='Set products', store=True, readonly=True)



    def create_single_products(self):
        # Nueva versión desde variantes desde atributo:
        for record in self:
            # 1. Chequeo variante parametrizada de empresa:
            param = env.user.company_id.product_attribute_id
            # Hay que pasar por todas las variantes para crear sus listas de materiales con los pares del surtido:
            for pr in record.product_variant_ids:
                # Cada variante tiene asociado probablemente algún surtido, lo buscamos:
                set = env['product.template.attribute.value'].search([('product_tmpl_id', '=', record.id),
                                                                      ('id', 'in', pr.product_template_variant_value_ids.ids),
                                                                      ('attribute_id', '=', param.id)]).product_attribute_value_id.set_template_id
                #  raise UserError(ptav_line.product_attribute_value_id.set_template_id.name)
                if set.id:
                    for li in set.line_ids:
                # jugar con value_id y quantity, o con el nombre que es un diccionario.
                # 1. Crear la lista de materiales si no existe.
                # 2. Buscar el pp_single relacionado para cada valor y rellenar el BOM.




        # Versión anterior (para sacar la creación del bom y eliminar):
        for te in self.set_template_ids:
            # Propuesta de código para el producto SURTIDO (SET):
            code = str(self.id) + self.set_code + te.code
            # Buscar línea de valor de atributo del producto, para la variante principal (habitualmente color o modelo):
            ptav1 = self.env['product.template.attribute.value'].search(
                [('product_tmpl_id', '=', self.id), ('product_attribute_value_id', '=', te.main_value_id.id)])
            # Comprobar si el producto SURTIDO ya estaba creado (búsqueda por referencia interna):
            exist = self.env['product.template'].search([('default_code','=', code)])
            if not exist.id:
                exist = self.env['product.template'].create({'name':code, 'default_code':code, 'barcode':code,
                                                             'detailed_type':'product',
                                                             'parent_id':self.id
                                                             })
            # Exista o sea nuevo, comprobamos si tiene la lista de materiales:
            if not exist.bom_ids.ids:
                new_bom = self.env['mrp.bom'].create({'code':code, 'type':'normal', 'product_qty':1,
                                                      'product_tmpl_id':exist.id,})
            # Mismo chequeo con las líneas bom:
            if not (exist.bom_ids.bom_line_ids.ids):
                # Crear las líneas del BOM tras haber buscado si existen las variantes en SELF:
                for va in te.line_ids:
                    # Búsqueda de línea de valor de atributo variable para cada talla de producto en SURTIDO:
                    ptav2 = self.env['product.template.attribute.value'].search(
                        [('product_tmpl_id', '=', self.id), ('product_attribute_value_id', '=', va.value_id.id)])
                    # Búsqueda de producto con ambos valores de atributo (principal y variable):
                    exist_pp = self.env['product.product'].search([('product_tmpl_id', '=', self.id),
                                                                   ('product_template_variant_value_ids', 'in', ptav1.id),
                                                                   ('product_template_variant_value_ids', 'in', ptav2.id)])
                    # Creación de línea de BOM, o ERROR de que la variante (talla) no existe:
                    if exist_pp.id:
                        new_bom_line = self.env['mrp.bom.line'].create({'bom_id': new_bom.id,
                                                                        'product_id': exist_pp.id,
                                                                        'product_qty': va.quantity,
                                                                        })
                    else:
                        raise UserError("No existe: " + va.name)
