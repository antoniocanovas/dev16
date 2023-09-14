from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('create_date','state')
    def _create_task_from_subscription(self):
        for record in self:
            if (record.state in ['draft','posted']):
                for li in record.invoice_line_ids:
                    create_task = False
                    # If subscription need task on DRAFT and not created before:
                    if not (li.task_id.id) and (li.subscription_id.create_task == 'draft') and (record.state == 'draft'):
                        create_task = True
                    # If subscription need task on POSTED and not created before:
                    if not (li.task_id.id) and (li.subscription_id.create_task == 'posted') and (record.state == 'posted'):
                        create_task = True
                    if create_task == True:
                        name = li.subscription_id.name + " - " + str(li.subscription_start_date)
                        newtask = self.env['project.task'].create({
                            'name':name,
                            'partner_id': record.partner_id.id,
                            'project_id': li.subscription_id.subscription_project_id.id,
                            'user_ids': [(6, 0, [li.subscription_id.subscription_project_id.user_id.id])],
                        })
                        li['task_id'] = newtask.id