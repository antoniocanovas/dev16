# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredential(models.Model):
    _name = "partner.credential"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Partner Credentials"

    name = fields.Char(string="Nombre", required=True, tracking=100)
    category_id = fields.Many2one('partner.credential.category', string="Category", required=True, tracking=100)
    partner_id = fields.Many2one("res.partner", string="Partner", tracking=100)
    user = fields.Char("User", tracking=100)

    encrypted = fields.Encrypted()
    password = fields.Char("Password", encrypt='encrypted')

    public = fields.Boolean("Public", tracking=100)
    url = fields.Char("Url", tracking=100)
    active = fields.Boolean("Active", default="True", tracking=100)
    description = fields.Text("Description", tracking=100)

    department_categ_ids = fields.Many2many(related='category_id.department_ids', string='Default users')
    department_ids = fields.Many2many("hr.department", string="Departments", tracking=100)
    @api.depends('password')
    def _get_pass_updated(self):
        for record in self:
            record['pass_updated'] = record.pass_updated +1
    pass_updated = fields.Integer("Password updated", store=True, tracking=100, compute="_get_pass_updated")

    @api.depends('department_ids', 'department_ids.member_ids', 'department_categ_ids', 'department_categ_ids.member_ids')
    def _get_department_users(self):
        users = []
        for dep in self.department_ids:
            for emp in dep.member_ids:
                if emp.user_id.id not in users:
                    users.append(emp.user_id.id)
        for dep in self.department_categ_ids:
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
