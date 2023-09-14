from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move'

    @api.depends('state')
    def _create_task_from_subscription(self):
        for record in self:
            if (record.state in ['draft','posted']):
                for li in record.invoice_line_ids:
                    create_task = False
                    # If subscription need task on DRAFT and not created before:
                    if not (li.task_id.id) and (li.subscription_id.task_create == 'draft') and (record.state == 'draft'):
                        create_task = True
                    # If subscription need task on POSTED and not created before:
                    if not (li.task_id.id) and (li.subscription_id.task_create == 'posted') and (record.state == 'posted'):
                        create_task = True
                    if create_task == True:
                        name = li.subscription_id.name + " - " + str(li.subscription_start_date)
                        raise UserError(name)
                        newtask = self.env['project.task'].create({
                            'name':name,
                            'partner_id': record.partner_id.id,
                            'project_id': li.subscription_id.subscription_project_id.id,
                        })
                        li['task_id'] = newtask.id