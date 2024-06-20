# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api, _


class CommissionPlan(models.Model):
    _inherit = "commission.plan"

    def action_open_commission_edit_wizard(self):
        self.ensure_one()

        return {
            "name": _("Edit Comission Wizard"),
            "view_mode": "form",
            "view_id": self.env.ref("custom_azarey.commission_plan_wizard_view").id,
            "view_type": "form",
            "res_model": "commission.plan.wizard",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_pnt_commission_plan_id": self.id,
            },
        }
