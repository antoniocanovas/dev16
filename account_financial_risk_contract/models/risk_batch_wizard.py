from odoo import _, api, fields, models


class RiskBatchWizard(models.TransientModel):
    _name = 'risk.batch.wizard'
    _description = 'Risk Batch add invoices Wizard'

    name = fields.Many2one('risk.batch', string='Name')
    invoice_ids = fields.Many2many('account.move', string='Invoices', store=True)

    def risk_batch_add_invoices_wizard_action(self):
        for record in self:
            return True