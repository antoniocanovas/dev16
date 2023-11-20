from odoo import _, api, fields, models
from datetime import datetime, date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Método para heredar comisionista del cliente:
    @api.depends('partner_id')
    def _get_default_commission_referrer(self):
        self.referred_id = self.partner_id.referred_id.id
    referred_id = fields.Many2one('res.partner', compute='_get_default_commission_referrer')

    # Método para heredar manager del comisionista:
    @api.depends('referred_id')
    def _get_commission_manager_id(self):
        self.manager_id = self.partner_id.referred_id.manager_id.id
    manager_id = fields.Many2one('res.partner', 'Manager', domain=[('grade_id', '!=', False)], tracking=True,
                                 compute='_get_commission_manager_id')

    manager_commission_plan_id = fields.Many2one(
        'commission.plan',
        'Manager Plan',
        compute='_compute_manager_commission_plan',
        inverse='_set_commission_plan',
        store=True,
        tracking=True,
        help="Takes precedence over the Manager's commission plan."
    )

    manager_commission = fields.Monetary(string='Referrer Commission', compute='_compute_manager_commission')


    @api.depends('commission_plan_frozen', 'partner_id', 'referrer_id', 'referrer_id.commission_plan_id', 'manager_id')
    def _compute_manager_commission_plan(self):
        for so in self:
            if not so.is_subscription and so.state in ['draft', 'sent']:
                so.manager_commission_plan_id = so.referrer_id.manager_id.manager_commission_plan_id
            elif so.is_subscription and not so.commission_plan_frozen:
                so.commission_plan_id = so.referrer_id.manager_id.manager_commission_plan_id


    @api.depends('referrer_id', 'commission_plan_id', 'sale_order_template_id', 'pricelist_id', 'order_line.price_subtotal',
                 'manager_id','manager_commission_plan_id')
    def _compute_manager_commission(self):
        self.manager_commission = 0
        for so in self:
            if not so.referrer_id or not so.commission_plan_id or not so.manager_id or not so.manager_commission_plan_id:
                so.manager_commission = 0
            else:
                comm_by_rule = defaultdict(float)
                template = so.sale_order_template_id
                template_id = template.id if template else None
                for line in so.order_line:
                    rule = so.manager_commission_plan_id._match_rules(line.product_id, template_id, so.pricelist_id.id)
                    if rule:
                        manager_commission = so.currency_id.round(line.price_subtotal * rule.rate / 100.0)
                        comm_by_rule[rule] += manager_commission

                # cap by rule
                for r, amount in comm_by_rule.items():
                    if r.is_capped:
                        amount = min(amount, r.max_commission)
                        comm_by_rule[r] = amount

                so.manager_commission = sum(comm_by_rule.values())
