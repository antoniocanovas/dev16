# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
import requests
from odoo.exceptions import ValidationError
from odoo import fields, models, api


import logging
_logger = logging.getLogger(__name__)


STATE = [
    ('DRAFT', 'DRAFT'),
    ('RECEIVED', 'RECEIVED'),
    ('ERROR', 'ERROR'),
    ('WAITING', 'WAITING'),
    ('WAITING_CHECK', 'WAITING_CHECK'),
    ('WAITING_CLIENT_SIGNATURE', 'WAITING_CLIENT_SIGNATURE'),
    ('REJECTED', 'REJECTED'),
    ('EXPIRED', 'EXPIRED'),
    ('DELETED', 'DELETED'),
    ('SENT', 'SENT'),
    ('RESPONSED', 'RESPONSED')
]

class Viafirma(models.Model):
    _name = 'viafirma'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Viafirma Model'

    name = fields.Char('Name')
    res_model = fields.Char('Origin Model')
    res_id = fields.Char('Origin ID')

    create_date = fields.Date(string="Create date")
    completed_date = fields.Date(string='Last change')

    state = fields.Selection(
        selection=STATE,
        string="State",
        default='DRAFT',
        tracking=True,
    )

    template_id = fields.Many2one('viafirma.templates')
    line_ids = fields.One2many(
        'viafirma.lines',
        'viafirma_id',
        string='Signers'
    )
    tracking_code = fields.Char(string='Tracking code')
    noti_text = fields.Char(string='Title')
    noti_detail = fields.Char(string='Description')
    notification_type_ids = fields.Many2many(
        comodel_name="viafirma.notification",
        string="Notification Type",
        domain=[('type', '=', 'notification')],
    )

    noti_subject = fields.Char(string='Subject')
    template_type = fields.Selection(selection=[('url','URL'),('base64','BASE64'),('message','MESSAGE')],string="Template Type",default='base64')

    #templareReference = fields.Char(defautl='"templateReference": ')  # este campo sirve para construir la linea que puede ser una url, base65 o un codigo
    #document_readRequired = fields.Boolean(string='Lectura obligatoria',default=False)
    #document_watermarkText = fields.Char(string='Marca de agua')
    #document_formRequired = fields.Boolean(string='Formulario',default=False)

    #document_policies = fields.Boolean(string='Send Policy')

    #viafirma_groupcode_id = fields.Many2one(
    #    'viafirma.groups',
    #    string="Group",
    #)

    document_to_send = fields.Binary("Document")
    document_signed = fields.Binary("Signed document")
    document_trail = fields.Binary("Trail document")
    error_code = fields.Char('Error')

    def viafirma_wizard(self):

        view_id = self.env.ref('viafirma.viafirma_wizard_view').id

        return {
            'name': "Wizard Viafirma",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'viafirma.wizard',
            'view_id': view_id,
            'target': 'new',

        }

    def send_viafirma(self):
        return

    def upd_viafirma(self):
        ''' chequeamos cada 5 minutos por cron el estado de los viafirma que no tengan estado RESPONSED (finalizado) para
        actualizar su estado cada cierto tiempo y ver si ha habido algun error'''

        viafirmas =self.env['viafirma'].search([('state', '!=', 'RESPONSED')])
        for via in viafirmas:
            via.status_response_firmweb()

    def get_uploader_header(self):

        header = {
            'Content-Type': 'application/json',
        }
        return header

    def compose_recipients(self, line_ids):
        recipients = []
        x = 0
        y = 1
        for recipient in line_ids.sorted(key=lambda l: l.id, reverse=True):
            recipient_n = {
                "key": str("FIRMANTE_") + str(x) + str(y) + str("_KEY"),
                "mail": recipient.email,
                "name": recipient.name,
            }
            if recipient.mobile:
                recipient_n.update({"phone": recipient.mobile})
            y += 1
            if y == 10:
                y = 0
                x += 1

            recipients.append(recipient_n)

        return recipients

    def compose_metadatalist_messages(self, line_ids):
        metadatalist = []
        x = 0
        y = 1
        theTemplate = self.template_id

        for recipient in line_ids.sorted(key=lambda l: l.id, reverse=True):
            for firma in theTemplate.firma_ids:
                if firma.value == 'email':
                    recipient_n = {
                        "key": str("FIRMANTE_") + str(x) + str(y) + str("_KEY"),
                        "value": recipient.name,
                    }
                    metadatalist.append(recipient_n)
                    if theTemplate.otp:
                        recipient_n = {
                            "key": str("MOBILE_SMS_") + str(x) + str(y),
                            "value": recipient.mobile
                        }
                        metadatalist.append(recipient_n)
            y += 1
            if y == 10:
                y = 0
                x += 1

        return metadatalist

    def compose_call(self):
        ''' tenemos que componer la llamada a la firma, por lo que tenemos que conocer el groupcode, el texto de la notificacion
            y a quien mandar dicha notificacion. Lo anterior no esta en el modelo Viafirma, como lo rellenaremos? A parte hemos de indicar quien recibirá la respuesta de la firma'''

        groupCode = {
            "groupCode": self.env.user.company_id.group_viafirma
        }
        workflow = {
            "workflow": {
                "type": "WEB",
            },
        }
        if len(self.notification_type_ids) > 1:
            notification = {
                "notification": {
                    "text": self.noti_text,
                    "detail": self.noti_detail,
                    "notificationType": "MAIL_SMS",
                    "sharedLink": {
                        "appCode": "com.viafirma.documents",
                        "email": self.line_ids.partner_id.email,
                        "phone": self.line_ids.partner_id.mobile,
                        "subject": self.noti_subject
                    }
                },
            }
        elif self.notification_type_ids[0].name == "SMS":
            notification = {
                "notification": {
                    "text": self.noti_text,
                    "detail": self.noti_detail,
                    "notificationType": self.notification_type_ids[0].name,
                    "sharedLink": {
                        "appCode": "com.viafirma.documents",
                        #"email": self.line_ids.partner_id.email,  #
                        "phone": self.line_ids.partner_id.mobile,
                        "subject": self.noti_subject
                    }
                },
            }
        else:
            notification = {
                "notification": {
                    "text": self.noti_text,
                    "detail": self.noti_detail,
                    "notificationType": self.notification_type_ids[0].name,
                    "sharedLink": {
                        "appCode": "com.viafirma.documents",
                        "email": self.line_ids.partner_id.email,
                        #"phone": self.line_ids.partner_id.mobile,
                        "subject": self.noti_subject
                    }
                },
            }
        metadatalist = {
            "metadataList": [{
                "key": "MOBILE_SMS_02", #Cambio 23/08/21
                "value": self.line_ids.partner_id.mobile
            }],
        }
        document = {
            "document": {
                "templateType": self.template_type,
                #"templateReference": "https://descargas.viafirma.com/documents/example/doc_sample_2018.pdf",
                "templateReference": str(self.document_to_send.decode('ascii')),
                "templateCode": self.template_id.code
            },
        }
        callbackmails = {
            "callbackMails": self.env.user.email,
        }
        callbackurl = {
            "callbackURL": ""
        }

        data = {**groupCode, **workflow, **notification, **metadatalist, **document, **callbackmails, **callbackurl }

        return data

    def compose_call_multiple(self):
        ''' tenemos que componer la llamada a la firma, por lo que tenemos que conocer el groupcode, el texto de la notificacion
            y a quien mandar dicha notificacion. Lo anterior no esta en el modelo Viafirma, como lo rellenaremos? A parte hemos de indicar quien recibirá la respuesta de la firma'''

        groupCode = {
            "groupCode": self.env.user.company_id.group_viafirma
        }
        workflow = {
            "workflow": {
                "type": "WEB",
            },
        }
        recip = self.compose_recipients(self.line_ids)

        recipients = {
            "recipients": recip,
        }

        customization = {
            "customization": {
                "requestMailSubject": str(self.name) + " - " + str(self.noti_text),
                "requestMailBody": "Hola {{recipient.name}}. <br /><br/>Ya puedes revisar y firmar el documento: <br /><br/>"
                                   + str(self.noti_text) + "<br /><br/>" + str(self.noti_detail) + "<br /><br/>" +
                                   "Haz click en el siguiente enlace y sigue las instrucciones.",
                "requestSmsBody": "En el siguiente link puedes revisar y firmar el documento",
                "callbackMailSuccessSubject": "Finalizado"  + " " + str(self.name) + str(self.noti_text),
                "callbackMailSuccessBody": "Hola {{recipient.name}}. <br /><br/>proceso finalizado: <br /><br/>"
                                   + str(self.noti_text) + "<br /><br/>" + str(self.noti_detail) + "<br /><br/>",
                "successMessage": "Proceso de firma completado",

            },
        }
        metadata = self.compose_metadatalist_messages(self.line_ids)

        messages ={
            "messages":[{
                "document": {
                    "templateType": self.template_type,
                    "templateReference": str(self.document_to_send.decode('ascii')),
                    "templateCode": self.template_id.code
                },
                "metadataList": metadata,
            #"policies": self.compose_policies() #comentado demo multiple sin enviar claves en blanco
            }]
        }
        callbackmails = {
            "callbackMails": self.env.user.email,
        }

        data = {**groupCode, **workflow, **recipients, **customization, **messages, **callbackmails}
        return data

    def compose_evidences(self, line_ids):
        ''' El maximo en Anchura es 596 puntos y en altura 838, teniendo en cuenta esta medidas por pagina, hay que divir el numero de firmantes entre este espacio'''

        theEvidences = []
        x = 0
        y = 1
        numSignatures = len(line_ids)
        # defino forWidth y forHigh para que el valor asignado no coincida con ninguna division por el numero de firmantes y confundir el codigo para que no
        # situe las cajas de firma en lugares equivocados equidistantes, por eso han de tomar 160 y 90 (valores fijos) segun el caso
        # quito 30 de cada margen horizontal, para que la firma se imprima sin problemas
        forWidth = (596 - 60) // numSignatures
        # para este caso la altura siempre la misma 90
        forHigh = 90
        # para el caso de que se firme en vertical, dejo el mismo margen de 30 por lado vertical oara que imprima sin problemas
        # forHigh = (838-60) // numSignatures
        # forWidth = 160
        # a partir de donde en horizontal se fijan las firmas, pegado al margen izquierdo la x, la y pegada al margen de abajo
        positionX = 30
        positionY = 68
        theTemplate = self.template_id
        for firma in theTemplate.firma_ids:
            for recipient in line_ids:
                numEvidence = 400 + (x * 1) + (y * 10)
                posMatch = 1000 + (x * 1) + (y * 10)
                if forWidth != 160:
                    positionX = 30 + (forWidth * (y - 1) * 1)
                if forHigh != 90:
                    positionY = 30 + (forHigh * (y - 1) * 1)
                if firma.value == 'email':
                    recipient_n = {
                        "type": "SIGNATURE",
                        "id": "evidence_" + str(numEvidence),
                        "enabledExpression": str("formItemIsNotEmpty('{{FIRMANTE_") + str(0) + str(y) + "_KEY}}','') ",
                        "enabled": "true",
                        "visible": "true",
                        "helpText": recipient.name,
                        "helpDetail": "Yo, " + recipient.name + ", acepto y firmo este documento.",
                        "positionsMatch": [{
                            "id": "positionmatch_" + str(posMatch),
                            "text": "firmante_" + str(x) + str(y),
                            "xoffset": 120,
                            "yoffset": -10,
                            "width": 60,
                            "height": 30
                        }],
                        "typeFormatSign": "XADES_B",
                        "recipientKey": "FIRMANTE_" + str(x) + str(y) + "_KEY"
                    }
                else:
                    numberIter = int((int(x) * 10) + int(y))
                    nIterac = numberIter - numSignatures
                    newx = nIterac // 10
                    newy = nIterac % 10
                    recipient_n = {
                        "type": "OTP_SMS",
                        "id": "evidence_" + str(numEvidence),
                        "enabled": "true",
                        "visible": "true",
                        # "helpText": "{{FIRMANTE_" + str(newx) + str(newy) + "_NAME}} Verificación SMS",
                        "helpText": recipient.name + " Verificación SMS",
                        # "positionsMatch" : [{
                        "positions": [{
                            # "id": "positionmatch_" + str(posMatch),
                            # "text": "la firma " + str(newx) + str(newy),
                            "rectangle": {
                                # "x": positionX,
                                "x": 60,
                                "y": positionY,
                                # "width": forWidth,
                                # "height": forHigh
                                "width": 30,
                                "height": 30
                            },
                            "page": -1
                        }],
                        "metadataList": [{
                            #"key": "phoneNumber",
                            "key": "{{MOBILE_SMS_" + str(x) + str(y) + "}}", #23/08/21
                            "value": recipient.mobile,
                            "internal": "false"
                        }],
                        "typeFormatSign": "XADES_B"
                    }
                theEvidences.append(recipient_n)
                y += 1
                if y == 10:
                    y = 0
                    x += 1

        return theEvidences

    def compose_policies(self):
        evidences = {
            "evidences": self.compose_evidences(self.line_ids)
        }

        signatures = {
            "signatures": [{
                "type": "SERVER",
                "helpText": "Sello Electrónico",
                "typeFormatSign": "PADES_LTA",
                "stampers": [{
                    "type": "TEXT",
                    # "rotation": "ROTATE_270",
                    "width": 38,
                    "height": 300,
                    "xAxis": 30,
                    "yAxis": 546,
                    "page": -1,
                    "timeZoneId": "Europe/Madrid"
                }],
                "lastUpdated": 0
            }]
        }

        data = [{**evidences, **signatures}]
        return data

    def compose_call_policies(self):
        ''' tenemos que componer la llamada a la firma, por lo que tenemos que conocer el groupcode, el texto de la notificacion
            y a quien mandar dicha notificacion. Lo anterior no esta en el modelo Viafirma, como lo rellenaremos? A parte hemos de indicar quien recibirá la respuesta de la firma'''

        groupCode = {
            "groupCode": self.env.user.company_id.group_viafirma
        }
        workflow = {
            "workflow": {
                "type": "WEB",
            },
        }
        recip = self.compose_recipients(self.line_ids)
        recipients = {
            "recipients": recip,
        }

        customization = {
            "customization": {
                "requestMailSubject": "Documento listo para firmar",
                "requestMailBody": "Hola {{recipient.name}}. <br /><br />Ya puedes revisar y firmar el documento. Haz click en el siguiente enlace y sigue las instrucciones.",
                "requestSmsBody": "En el siguiente link puedes revisar y firmar el documento"
            },
        }
        metadata = self.compose_metadatalist_messages(self.line_ids)
        messages = {
            "messages": [{
                "document": {
                    "templateType": self.template_type,
                    "templateReference": str(self.document_to_send.decode('ascii')),
                    "templateCode": self.template_id.code
                },
                "metadataList": metadata,
                "policies": self.compose_policies()
            }]
        }
        callbackmails = {
            "callbackMails": self.env.user.email,
        }

        data = {**groupCode, **workflow, **recipients, **customization, **messages, **callbackmails}

        return data

    def download_document(self, url, header, response_code, viafirma_user, viafirma_pass):

        r_doc = requests.get(url, headers=header, auth=(viafirma_user, viafirma_pass))
        if r_doc.ok:
            rr_doc = json.loads(r_doc.content.decode('utf-8'))

        response = requests.get(rr_doc["link"], headers=header)
        if response.status_code == 200:
            img_file_encode = base64.b64encode(response.content)
            return img_file_encode

    def status_response_firmweb(self):
        ''' Esta funcion ha de obtener el estado de la peticion'''

        header = self.get_uploader_header()
        response_code = self.tracking_code
        search_url = 'https://services.viafirma.com/documents/api/v3/messages/status/' + str(response_code)

        viafirma_user = self.env.user.company_id.user_viafirma
        viafirma_pass = self.env.user.company_id.pass_viafirma

        if viafirma_user:
            if viafirma_pass:

                stat_firmweb = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
                if stat_firmweb.ok:
                    statu_firmweb = json.loads(stat_firmweb.content.decode('utf-8'))
                    # de momento lo hago con la primera line_ids que hay
                    for line in self.line_ids:
                        line.state = statu_firmweb["status"]
                    # El estado de viafirma depende de los estados de las líneas
                    self.state = statu_firmweb["status"]
                    # statu_firmweb["status"] contiene el estado actual de la peticion y que me puede servir para cambiar el campo viafirma.status
                    if statu_firmweb["status"] == 'RESPONSED':
                        # ya ha sido firmada me puedo descargar el documento firmado y el trail de la firma
                        # empezamos por el documento firmado
                        url = 'https://services.viafirma.com/documents/api/v3/documents/download/signed/' + response_code

                        self.document_signed = self.download_document(  url,  header, response_code, viafirma_user, viafirma_pass)
                        # ahora le toca el turno al documento de trail, pero para este documento no hay campo en el modelo viafirma, lo dejo preparado
                        url = 'https://services.viafirma.com/documents/api/v3/documents/download/trail/' + response_code
                        self.document_trail = self.download_document(url, header, response_code, viafirma_user,
                                                                         viafirma_pass)
                    elif statu_firmweb['status'] == 'ERROR':
                        # guardar el resultado de error en un campo para su visualizacion
                        url = 'https://services.viafirma.com/documents/api/v3/messages/' + response_code
                        r_error = requests.get(url, headers=header, auth=(viafirma_user, viafirma_pass))

                        if r_error.ok:
                            rr_error = json.loads(r_error.content)
                            # los dos campos de este dictionary interesantes son message y trace
                            self.error_code = rr_error["workflow"]["history"]
                else:
                    self.error_code = json.loads(stat_firmweb.content.decode('utf-8'))
        else:
            raise ValidationError(
                "You must set Viafirma login Api credentials")

    def check_mandatory_attr(self, method, partner_id, otp):
        if otp:
            value = getattr(partner_id, 'mobile')
            if not value:
                raise ValidationError(
                    "mobile is mandatory for OTP/SMS")
        for attr in method:
            try:
                value = getattr(partner_id, attr.value)
            except Exception as e:
                raise ValidationError(
                    "Server Error : %s" % e)
            if not value:
                raise ValidationError(
                    "%s is mandatory for this template" % attr.value)

    def check_template(self):
        if self.template_id:
            if not self.template_id.firma_ids:
                raise ValidationError(
                    "Please select a signature method on Viafirma Template")
        else:
            raise ValidationError(
                "Please select a Viafirma Template")

    def call_viafirma(self):
        ''' solo firma web y un solo firmante, la mas simple de todas, de momento selecciono todos los registros que tenga en el modelo viafirma y que haga el proceso
         de envio para cada uno de ellos, aunque no coge ningun valor de estos, ni emqail ni adjunto'''

        #Comprobamos todas las restricciones para informar al ususario antes de iniciar ejecución
        self.check_template()

        if not self.env['viafirma.templates'].updated_templates(self.template_id.code):
            raise ValidationError(
                "Template no existe")

        if self.line_ids:
            for line in self.line_ids:
                self.check_mandatory_attr(self.template_id.firma_ids, line.partner_id, self.template_id.otp )
                self.check_mandatory_attr(self.notification_type_ids, line.partner_id, False)
            if not self.document_to_send:
                raise ValidationError(
                    "Need a binary to send")

            viafirma_user = self.env.user.company_id.user_viafirma
            viafirma_pass = self.env.user.company_id.pass_viafirma

            if viafirma_user:
                if viafirma_pass:
                    header = self.get_uploader_header()

                    #if self.template_id.multiple_signatures:
                    search_url = 'https://services.viafirma.com/documents/api/v3/set/'
                    datas = self.compose_call_multiple()

                    response_firmweb = requests.post(search_url, data=json.dumps(datas), headers=header,
                                                     auth=(viafirma_user, viafirma_pass))

                    if response_firmweb.ok:
                        resp_firmweb = json.loads(response_firmweb.content.decode('utf-8'))

                        # normalmente devuelve solo un codigo pero puede ser que haya mas, ese código hay que almacenarlo en viafirma.status_id para su posterior consulta de estado
                        try:
                            if resp_firmweb["messages"][0]["code"] != '':
                                self.tracking_code = resp_firmweb["messages"][0]["code"]
                        except:
                            self.tracking_code = resp_firmweb
                        self.status_response_firmweb()
                    else:
                        self.error_code = json.loads(response_firmweb.content.decode('utf-8'))

            else:
                raise ValidationError(
                            "You must set Viafirma login Api credentials")
        else:
            raise ValidationError(
                "No hay firmantes seleccionados")


    #def compose_metadatalist(self, line_ids):
    #    metadatalist = []
    #    x = 0
    #    y = 1
    #    for recipient in line_ids:
    #        recipient_n = {
    #             "key": str("FIRMANTE_") + str(x) + str(y) + str("_NAME"),
    #             "value":  recipient.name,
    #        }
    #        metadatalist.append(recipient_n)
    #        y += 1
    #        if y == 10:
    #            y = 0
    #            x += 1
    #
    #    return metadatalist