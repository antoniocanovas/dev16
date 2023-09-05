# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import json
import requests
from odoo.exceptions import ValidationError


# la consulta a tecdoc devuelve todos los coches de la serie, por lo que deberia de haber un modelo coche, quye pertenezca a una marca, modelo y serie determinada
class ViafirmaTemplates(models.Model):
    _name = 'viafirma.templates'
    _description = 'Viafirma Templates'

    name = fields.Char('Name')
    code = fields.Char('Code')
    description = fields.Char('Description')
    firma_ids = fields.Many2many(
        comodel_name="viafirma.signature",
        string="Signatures",
        domain=[('type', '=', 'signature')],
    )
    #num_firmantes = fields.Integer('Numero firmantes')

    multiple_signatures = fields.Boolean('Multiple Signatures')
    otp = fields.Boolean(string='OTP/SMS')

    def get_uploader_header(self):

        header = {
            'Content-Type': 'application/json',
        }
        return header

    def deleteOldTemplates(self, listCodes):
        ''' Recorro todos los registros del modelo y busco coincidencias con lo traido desde la api, sino hay coincidencia se borra el registro '''
        allTemplates = self.env['viafirma.templates'].search([])
        for template in allTemplates:
            if template.code not in listCodes:
                self.search([('code', '=', template.code)]).unlink()

    def create_templates(self, thedict):
        '''Esta funcion actualiza las plantillas y crea las nuevas'''
        # chequeo si no viene description para dejarlo en un str vacio
        try:
            if not thedict["description"]:
                pass
        except:
            thedict["description"] = ""

        existe = self.env['viafirma.templates'].search([('code', '=', thedict["code"])])
        if not existe:
            viafirma_template_id = self.env['viafirma.templates'].create({
                'name': thedict["title"],
                'code': thedict["code"],
                'description': thedict["description"]
            })
        else:
            viafirma_template_id = existe.write({
                'name': thedict["title"],
                'code': thedict["code"],
                'description': thedict["description"]
            })
            return viafirma_template_id

    def updated_templates(self, checkCode = ""):

        ''' add checkCode para buscar en caso de llamada si existe la plantilla antes de la llamada '''

        viafirma_user = self.env.user.company_id.user_viafirma
        viafirma_pass = self.env.user.company_id.pass_viafirma

        canLaunch = False # lo utilizo para saber si esta operativa la plantilla y poder lanzar
        listAllTemplatesAPI = [] # la utilizo para saber todos los codigo de templates que he descargado

        if viafirma_user:
            if viafirma_pass:
                if self.env.user.company_id.api_viafirma_user:
                    header = self.get_uploader_header()
                    search_url = 'https://services.viafirma.com/documents/api/v3/template/list/'\
                                 + self.env.user.company_id.api_viafirma_user
                    response_template = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
                    if response_template.ok:
                        resu_templates = json.loads(response_template.content)
                        for resu_template in resu_templates:
                            listAllTemplatesAPI.append(resu_template["code"])
                            self.create_templates(resu_template)
                            if resu_template["code"] == checkCode:
                                canLaunch = True
                        self.deleteOldTemplates(listAllTemplatesAPI)
                    else:
                        raise ValidationError(
                            "Problemas en el sistema Viafirma")
                        return False
                else:
                    raise ValidationError(
                        "No API user defined, please check your company configuration on Viafirma tab")
                    return False


        return canLaunch