# Copyright

import base64
import codecs
from PIL import Image
import io
from odoo import fields, models, api
from odoo.exceptions import ValidationError

TYPE = [
    ('upload', 'Upload'),
    ('url', 'Url'),
    ('viafirma', 'Viafirma'),
]

class ViafirmaWizard(models.TransientModel):
    _name = 'viafirma.wizard'
    _description = 'Viafirma creation wizard'


    name = fields.Char('Name')

    template_id = fields.Many2one('viafirma.templates')
    line_ids = fields.Many2many(
        'res.partner',
        string='Signers'
    )
    document_unique = fields.Boolean(
        'One for user',
        help='Send one viafirma for user, instead the same viafirma for all users',
    )
    notification_type_ids = fields.Many2many(
        comodel_name="viafirma.notification",
        string="Notification type",
        domain=[('type', '=', 'notification')],
    )
    noti_subject = fields.Char(string='Subject')

    document_type = fields.Selection(
        selection=TYPE,
        string="Document Type",
        default='upload',
    )
    document_type_text = fields.Char('Type of document',compute='check_type')
    document_to_send = fields.Binary("Document")

    res_model = fields.Char('Model')
    company_signed = fields.Boolean("Company signed")

    viafirma_doc_id = fields.Integer('Viafirma doc id')

    @api.depends('document_type')
    def check_type(self):
        for record in self:
            if record.document_type == 'upload':
                record.document_type_text = 'upload'
            if record.document_type == 'url':
                record.document_type_text = 'url'
            if record.document_type == 'viafirma':
                record.document_type_text = 'viafirma'

    def create_viafirma(self):

        if self.document_type == 'upload':
            template_type='base64'
        if self.res_model:
            res_model = self.res_model
            policy = True
        else:
            res_model = 'Wizard'
            policy = False

        if self.document_unique:
            for partner in self.line_ids:
                line_ids = []
                line_id = self.env['viafirma.lines'].create(
                    {
                        'partner_id': partner.id,
                        #'viafirma_id': viafirma_id.id,
                    }
                )
                line_ids.append(line_id.id)
                if self.company_signed:
                    line_id = self.env['viafirma.lines'].create({
                        'partner_id': self.env.user.company_id.partner_id.id,
                        # 'viafirma_doc_id': self.id,
                    })
                    line_ids.append(line_id.id)
                viafirma_id = self.env['viafirma'].create({
                    'name': str(self.env.user.name) + '-' + str(self.name) + ' for ' + str(partner.name),
                    'noti_text': str(self.name) + ' for ' + str(partner.name),
                    'noti_subject': str(self.name) + ' for ' + str(partner.name),
                    'noti_detail': str(self.name) + ' for ' + str(partner.name),
                    'template_id': self.template_id.id,
                    'notification_type_ids': [(6, 0, self.notification_type_ids.ids)],
                    'line_ids': [(6, 0, line_ids)],
                    'template_type': template_type,
                    'document_to_send': self.document_to_send,
                    'viafirma_doc_id': self.viafirma_doc_id,
                    'res_model': res_model,
                    'res_id': False,
                    # 'res_id_name': str(self.name),
                    'document_policies': policy,
                })
        else:
            line_ids = []
            for line in self.line_ids:
                line_id = self.env['viafirma.lines'].create(
                    {
                        'partner_id': line.id,
                        #'viafirma_id': viafirma_id.id,
                    }
                )
                line_ids.append(line_id.id)
            if self.company_signed:
                line_id = self.env['viafirma.lines'].create({
                    'partner_id': self.env.user.company_id.partner_id.id,
                    #'viafirma_doc_id': self.id,
                })
                line_ids.append(line_id.id)

            viafirma_id = self.env['viafirma'].create({
                'name': str(self.env.user.name) + '-' + str(self.name),
                'noti_text': str(self.env.user.name) + '-' + str(self.name),
                'noti_subject': str(self.env.user.name) + '-' + str(self.name),
                'template_id': self.template_id.id,
                'notification_type_ids':[(6, 0, self.notification_type_ids.ids)],
                'line_ids': [(6, 0, line_ids)],
                'template_type': template_type,
                'document_to_send': self.document_to_send,
                'viafirma_doc_id': self.viafirma_doc_id,
                'res_model': res_model,
                'res_id': False,
                #'res_id_name': str(self.name),
                'document_policies': policy,
            })



