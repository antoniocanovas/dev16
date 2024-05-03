# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredential(models.Model):
    _name = "partner.credential"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Partner Credentials"

    name = fields.Char(string="Nombre", required=True)
    category_id = fields.Many2one('partner.credential.category', string="Category", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner")
    user = fields.Char("User")
    password = fields.Char("Password")
    public = fields.Boolean("Public")
    url = fields.Char("Url")
    active = fields.Boolean("Active", default="True")
    description = fields.Text("Description")

    @api.onchange('category_id')
    def _get_default_departments(self):
        self.department_ids = [(6,0,category_id.department_ids.ids)]
    department_ids = fields.Many2many("hr.department", string="Departments", compute='_get_default_departments', index=True)

    @api.depends('department_ids', 'department_ids.member_ids')
    def _get_department_users(self):
        users = []
        for dep in self.department_ids:
            for emp in dep.member_ids:
                if emp.user_id.id not in users:
                    users.append(emp.user_id.id)
        self.user_ids = [(6,0,users)]
    user_ids = fields.Many2many("res.users", string="Users", store=True, compute="_get_department_users")

    def _user_can_edit(self):
        for record in self:
            admin_group = self.env.ref('partner_credential.admin_credential_group')
            edit = False
            if (self.env.user == record.create_uid): edit = True
            if (admin_group.users.ids) and (self.env.user in admin_group.users): edit = True
            record['user_can_edit'] = edit
    user_can_edit = fields.Boolean('Edit', compute='_user_can_edit')

    def action_view_password(self):
        action = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Copy quickly !!",
                "message": self.password,
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
        return action
