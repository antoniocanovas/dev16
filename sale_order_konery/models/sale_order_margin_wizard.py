from odoo import _, api, fields, models

#TYPE = [
#    ('services', 'Final price applying discounts on services'),
#    ('discount', 'Discount'),
#]


class SaleMarginWizard(models.TransientModel):
    _name = 'sale.order.margin.wizard'
    _description = 'Sale Order Margin Wizard'

    #Campos con duda
    name = fields.Char('Name')
    #Campos
    sale_id = fields.Many2one('sale.order')
    general_margin = fields.Float('General Margin')
    product_margin = fields.Float('Product Margin')


#    discount = fields.Float('Discount')
#    childs = fields.Boolean('Childs')
#    products = fields.Boolean('Products')
#    services = fields.Boolean('Services')
#    all_quotation = fields.Boolean('All Quotation')
#    price = fields.Float('Price')
#    type = fields.Selection(selection=TYPE, string="Type")
#    section_id = fields.Many2one('sale.order.line', string='Section')



