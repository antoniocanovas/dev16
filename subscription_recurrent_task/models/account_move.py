from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move'

    @api.depends('state')
    def _create_task_from_subscription(self):
        if (self.state in ['draft','posted']):
            for li in self.invoice_line_ids:
                create_task = False
                # If subscription need task on DRAFT and not created before:
                if not (li.task_id.id) and (li.subscription_id.task_create == 'draft') and (self.state == 'draft'):
                    create_task = True
                # If subscription need task on POSTED and not created before:
                if not (li.task_id.id) and (li.subscription_id.task_create == 'posted') and (self.state == 'posted'):
                    create_task = True
                if create_task == True:
                    name = li.subscription_id.name + " - " + str(li.subscription_start_date)
                    newtask = self.env['project.task'].create({
                        'name':name,
                        'partner_id': self.partner_id.id,
                        'project_id': li.subscription_id.subscription_project_id.id,
                    })
                    li['task_id'] = newtask.id