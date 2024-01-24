# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Campos requeridos para la importación de productos, para borrar tras terminar:
    mig_peso = fields.Integer('mig_peso')
    mig_partidaarancelaria = fields.Integer('mig_partidaarancelaria')
    mig_msgbloqueo = fields.Char('mig_msgbloqueo')
    mig_imagen = fields.Char('mig_imagen')
    mig_material = fields.Integer('mig_material')
    mig_costefab = fields.Monetary('mig_costefab')
    mig_costetrans = fields.Monetary('mig_costetrans')
    mig_manufacturer = fields.Char('mig_manufacturer')

