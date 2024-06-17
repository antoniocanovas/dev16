# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ProductBrand(models.Model):
    _inherit = "res.partner"

    # Para borrar después de la migración:
    mig_provincia = fields.Char(string='mig_provincia', store=True)
    mig_pais = fields.Char(string='mig_pais', store=True)
    mig_fax = fields.Char(string='mig_fax', store=True)
    mig_nif = fields.Char(string='mig_nif', store=True)
    mig_autorizacion_sepa = fields.Char(string='mig_autorizacion_sepa', store=True)
    mig_tarifa = fields.Char('mig_tarifa', store=True)
    mig_recargo = fields.Char(string='mig_recargo', store=True)
    mig_nomban = fields.Char(string='mig_nomban', store=True)
    mig_ccc = fields.Char(string='mig_ccc', store=True)
    mig_iban = fields.Char(string='mig_iban', store=True)
    mig_riesgo = fields.Char(string='mig_riesgo', store=True)
    mig_formapago = fields.Char(string='mig_formapago', store=True)
    mig_representante = fields.Char(string='mig_representante', store=True)
    mig_fechasepa = fields.Char(string='mig_fechasepa', store=True)
    mig_comision = fields.Float(string='mig_comision', store=True)
    mig_repreiva = fields.Integer(string='mig_repreiva', store=True)
    mig_contrapartida = fields.Char(string='mig_contrapartida', store=True)
    mig_nivel = fields.Integer(string='mig_nivel', store=True)
    mig_nombreaeat = fields.Char(string='mig_nombreaeat', store=True)
