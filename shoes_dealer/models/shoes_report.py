# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ShoesSaleReport(models.Model):
   _name = 'shoes.sale.report'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = 'Shoes Sale Report'


   name = fields.Char(string='Nombre', required=True)
   shoes_campaign_id = fields.Many2one('project.project', string='Shoes campaign')
   model_ids = fields.One2many('shoes.sale.report', 'shoes_report_id', string='Lines')
   @api.depends('shoes_campaing_id')
   def _get_sale_orders(self):
       for record in self:
           orders = self.env['sale.order'].search([
               ('shoes_campaign_id','=',record.shoes_campaign_id.id),
               ('state','not in', ['draft','cancel']),
           ])
           record['sale_ids'] = [(6,0,orders.ids)]
   sale_ids = fields.Many2many('sale.order', string='Orders', compute='_get_sale_orders')



# Campos calculados para mostrar en el informe de "Rentabilidad por pedidos":
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_shoes_sale_percent_discount(self):
        for record in self:
            discount = 0
            if record.amount_untaxed != 0:
                discount = (1 - (record.amount_untaxed * 100 / record.amount_undiscounted)) * 100
            record['global_discount'] = discount
    global_discount = fields.Float(string='Global discount', store=False, compute='_get_shoes_sale_percent_discount')

    def _get_shoes_sale_amount_discounted(self):
        for record in self:
            record['amount_discounted'] = record.amount_undiscounted - record.amount_untaxed
    amount_discounted = fields.Float(string='Discounted amount', store=False, compute='_get_shoes_sale_amount_discounted')


    def _get_shoes_referrer_percent_commission(self):
        for record in self:
            commission = 0
            if (record.amount_untaxed != 0) and (record.commission != 0):
                commission = (1 - (record.commission * 100 / record.amount_untaxed)) * 100
            record['referrer_percent_commission'] = commission
    referrer_percent_commission = fields.Float('Referrer Com', store=False, compute='_get_shoes_referrer_percent_commission')

    def _get_shoes_manager_percent_commission(self):
        for record in self:
            commission = 0
            if (record.amount_untaxed != 0) and (record.manager_commission != 0):
                commission = (1 - (record.manager_commission * 100 / record.amount_untaxed)) * 100
            record['manager_percent_commission'] = commission
    manager_percent_commission = fields.Float('Manager Com', store=False, compute='_get_shoes_manager_percent_commission')


    def _get_amount_without_commission(self):
        for record in self:
            record['amount_whitout_commission'] = record.amount_untaxed - record.commission - record.manager_commission
    amount_whitout_commission = fields.Float('Net amount', store=False, compute='_get_amount_without_commission')

    def _get_cost_before_delivery(self):
        for record in self:
            cost = 0
            for li in record.order_line:
                if li.product_id.product_tmpl_set_id.id or li.product_id.product_tmpl_single_id.id:
                    cost += li.product_id.standard_price * li.product_uom_qty
            record['cost_before_delivery'] = cost
    cost_before_delivery = fields.Monetary('Cost', store=False, compute='_get_cost_before_delivery')

    def _get_shoes_sale_margin(self):
        record['shoes_margin'] = record.amount_untaxed - record.commission - record.manager_commission - record.cost_before_delivery
    shoes_margin = fields.Monetary('Shoes margin', store=False, compute='_get_shoes_sale_margin')

    def _get_shoes_margin_percent(self):
        for record in self:
            margin = 0
            if (record.amount_untaxed != 0):
                margin = (1 - (record.shoes_margin / record.amount_untaxed)) * 100
            record['shoes_margin_percent'] = margin
    shoes_margin_percent = fields.Float('Margin (%)', store=False, compute='_get_shoes_margin_percent')






# Campos calculados para mostrar en el informe de "Rentabilidad por modelos":
class ShoesSaleReportLine(models.Model):
    _name = 'shoes.sale.report.line'
    _description = 'Shoes Sale Report Line'

    shoes_report_id = fields.Many2one('shoes.sale.report', string='Shoes report')
    model_id = fields.Many2one('product.template', string='Model')
    color_id = fields.Many2one('product.attribute.value', string='Color', related='model_id.color_attribute_id')
    model_description = fields.Text('Sale description', related='model_id.description_sale')
    sale = fields.Monetary('Sale amount')
    discount = fields.Monetary('Discount amount')
    discount_early_payment = fields.Monetary('PP discount')
    referrer = fields.Monetary('Referrer amount')
    manager = fields.Monetary('Manager amount')
    total = fields.Monetary('Net amount')
    cost = fields.Monetary('Cost amount')
    margin = fields.Monetary('Margin amount')
    margin_percent = fields.Float('Margin %')
    pairs_count = fields.Integer('Pairs')
