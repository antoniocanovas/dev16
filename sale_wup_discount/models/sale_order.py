from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

VALUES = [
    ('fixed_service_margin_over_cost', 'Fixed price for "our services", and margin over cost for others.'),
    ('margin_over_cost', 'Margin over cost.'),
    ('target_price', 'Target price.'),
    ('target_price_with_fixed_services', 'Target price with fixed services (overwrite locked sale price in wups)'),
    ('wup_pricing_reset', 'Reset WUPs (prices & fixeds).'),
]


class WupSaleOrder(models.Model):
    _inherit = 'sale.order'

    target_price = fields.Monetary('Target price', currency_field='currency_id')
    price_our_service = fields.Monetary(string='Price our service')
    margin_wup_percent = fields.Float('Margin')
    discount_type = fields.Selection(
        selection=VALUES, string="Type",
    )

    def wup_sale_discounts(self):
        for record in self:
            # Round prices with Odoo monetary_precision:
            monetary_precision = self.env['decimal.precision'].sudo().search([('id', '=', 1)]).digits

            # CASE "TARGET_PRICE" (wup prices are not recalculated, working with discount in SOL):
            if record.discount_type == 'target_price':
                # PREVIOUS: Compute real total cost and sale without discount:
                cost_amount, price_amount, margin_wup_percent, message_under_cost = 0, 0, 0, ""
                for li in record.order_line:
                    if (len(li.wup_line_ids.ids) == 0) and (li.product_uom_qty > 0):
                        cost_amount += li.price_unit_cost * li.product_uom_qty
                        price_amount += li.lst_price * li.product_uom_qty
                    elif (len(li.wup_line_ids.ids) > 0) and (li.product_uom_qty > 0):
                        cost_amount += round(li.wup_cost_amount, monetary_precision)
                        price_amount += round(li.price_subtotal / (1 - li.discount / 100), monetary_precision)

                # CASE SALE UNDER COST, NOT ALLOWED:
                if (record.target_price < cost_amount):
                    message_under_cost = "Target under real cost (Purchase = " + str(
                        round(cost_amount, monetary_precision)) + ", List price = " + str(
                        round(price_amount, monetary_precision)) + "), not allowed. You can do it manually."
                    raise ValidationError(message_under_cost)

                # CASE: TARGET UNDER PVP => Let's work with discounts:
                elif (record.target_price < price_amount):
                    margin = (1 - (record.target_price / price_amount)) * 100
                    for li in record.order_line:
                        if (len(li.wup_line_ids.ids) == 0) and (li.product_uom_qty > 0):
                            li.write({'price_unit': li.lst_price, 'discount': margin})
                        elif (len(li.wup_line_ids.ids) > 0) and (li.product_uom_qty > 0):
                            sol_price_unit_from_wup = 0
                            for wupline in li.wup_line_ids:
                                wup_price_unit = wupline.price_unit * (1 - margin / 100)
                                sol_price_unit_from_wup += wup_price_unit * wupline.product_uom_qty
                                wupline['price_unit'] = wup_price_unit
                            li.write({'price_unit':sol_price_unit_from_wup, 'discount':0})

                # CASE: TARGET UNDER PVP => Let's work with list prices:
                else:
                    margin = (record.target_price / price_amount)
                    for li in record.order_line:
                        if (len(li.wup_line_ids.ids) == 0) and (li.product_uom_qty > 0):
                            li.write({'price_unit': li.lst_price * margin, 'discount': 0})
                        elif (len(li.wup_line_ids.ids) > 0) and (li.product_uom_qty > 0):
                            sol_price_unit_from_wup = 0
                            for wupline in li.wup_line_ids:
                                wupline.write({'price_unit': wupline.price_unit * margin, 'fix_price_unit_sale': False})
                                sol_price_unit_from_wup += wupline.price_unit * margin * wupline.product_uom_qty
                            li.write({'price_unit':sol_price_unit_from_wup, 'discount':0})

                # ROUNDING Method on the first line with units = 1:
                diference = round(record.target_price - record.amount_untaxed, monetary_precision)
                if diference != 0:
                    review = True
                    for li in record.order_line:
                        if (li.product_uom_qty == 1) and (review == True):
                            if (len(li.wup_line_ids.ids) == 0) and (li.product_uom_qty > 0):
                                li.write({'price_unit': li.price_unit + diference})
                                review = False
                            elif (len(li.wup_line_ids.ids) > 0) and (li.product_uom_qty > 0):
                                for wupline in li.wup_line_ids:
                                    if (review == True):
                                        wupline.write({'price_unit': wupline.price_unit + diference})
                                        review = False
            # END CASE "TARGET_PRICE" !!

            # CASE WUP_PRICING_RESET:
            elif record.discount_type == 'wup_pricing_reset':
                for li in record.order_line:
                    if li.wup_line_ids.ids:
                        sol_price_unit_from_wup = 0
                        for wul in record.wup_line_ids:
                            sol_price_unit_from_wup += wul.product_id.list_price * wul.product_uom_qty
                            wul.write({'price_unit': wul.product_id.list_price,
                                      'price_unit_cost': wul.product_id.standard_price,
                                      'fix_price_unit_cost': False, 'fix_price_unit_sale': False})
                        li.write({'price_unit':sol_price_unit_from_wup, 'discount':0})
            # END CASE WUP_PRICING_RESET !!

            # CASE FIX OUR SERVICES AND GLOBAL TARGET PRICE:
            elif record.discount_type == 'target_price_with_fixed_services':
                # Our service subtotal and writting:
                fixed_qty, prev_other_subtotal, ratio, fixed = 0, 0, 1, record.price_our_service

                # ESTIMATIONS AND RATIO:
                for li in record.order_line:
                    # Lines NOT WUP and our_service True:
                    if (li.product_id.id) and not (li.wup_line_ids.ids) and (li.product_uom_qty > 0) and (
                            li.product_id.our_service == True):
                        fixed_qty += li.product_uom_qty
                    # Lines NOT WUP and our_service False:
                    elif (li.product_id.id) and not (li.wup_line_ids.ids) and (li.product_uom_qty > 0) and (
                            li.product_id.our_service == False):
                        prev_other_subtotal += li.price_unit * li.product_uom_qty
                    # WUP Lines:
                    elif (li.product_id.id) and (len(li.wup_line_ids.ids) != 0):
                        for wup in li.wup_line_ids:
                            if (wup.product_id.our_service == True):
                                fixed_qty += wup.product_uom_qty
                            else:
                                prev_other_subtotal += wup.subtotal

                if prev_other_subtotal != 0:
                    ratio = (record.target_price - fixed_qty * fixed) / prev_other_subtotal

                # Writing new values:
                for li in record.order_line:
                    # Lines NOT WUP and our_services True:
                    if (li.product_id.id) and not (li.wup_line_ids.ids) and (li.product_uom_qty > 0) and (
                            li.product_id.our_service == True):
                        li.write({'price_unit': fixed, 'discount': 0, 'price_subtotal': li.product_uom_qty * fixed})
                    # Lines NOT WUP and our_services False:
                    elif (li.product_id.id) and not (li.wup_line_ids.ids) and (li.product_uom_qty > 0) and (
                            li.product_id.our_service == False):
                        price_unit = li.price_unit * ratio
                        li.write({'price_unit': price_unit, 'discount': 0})
                    # WUP Lines:
                    elif (li.product_id.id) and (len(li.wup_line_ids.ids) != 0):
                        li.write({'discount': 0})
                        for wup in li.wup_line_ids:
                            if (wup.product_id.our_service == True):
                                wup.write({'price_unit': fixed, 'subtotal': fixed * wup.product_uom_qty})
                            else:
                                price_unit = wup.price_unit * ratio / li.product_uom_qty
                                wup.write({'price_unit': price_unit, 'subtotal': price_unit * wup.product_uom_qty})

                # ROUNDING Method on the first line with units = 1:
                diference = round(record.target_price - record.amount_untaxed, monetary_precision)
                if diference != 0:
                    review = True
                    for li in record.order_line:
                        if (li.product_uom_qty == 1) and (review == True):
                            if (len(li.wup_line_ids.ids) == 0) and (li.product_uom_qty > 0):
                                li.write({'price_unit': li.price_unit + diference})
                                review = False
                            elif (len(li.wup_line_ids.ids) > 0) and (li.product_uom_qty > 0):
                                for wupline in li.wup_line_ids:
                                    if (review == True):
                                        wupline.write({'price_unit': wupline.price_unit + diference})
                                        review = False
            # END CASE fixed_services_and_target_price !!


            # CASES FIX_OUR_SERVICES (or not) AND MARGIN_OVER_COST:
            else:
                for li in record.order_line:
                    # If we use type, there is not line discount:
                    if (li.discount != 0):
                        li['discount'] = 0

                    # Line is NOT WUP:
                    if (len(li.wup_line_ids.ids) == 0) and (li.product_uom_qty > 0):
                        ratio = 1
                        if li.product_uom.id != li.product_id.uom_id.id:
                            # uom_type: bigger, reference, smaller
                            if li.product_id.uom_id.uom_type == 'smaller':
                                ratio = ratio / li.product_id.uom_po_id.factor
                            elif li.product_id.uom_id.uom_type == 'bigger':
                                ratio = ratio * li.product_id.uom_po_id.factor_inv
                            if li.product_uom.uom_type == 'smaller':
                                ratio = ratio * li.product_uom.factor
                            elif li.product_uom.uom_type == 'bigger':
                                ratio = ratio / li.product_uom.factor_inv


                        # Case 'services' and 'fixed_service_price':
                        if (li.product_id.product_tmpl_id.our_service == True) and (
                                record.discount_type == 'fixed_service_margin_over_cost'):
                            price_unit = round(record.price_our_service / ratio, monetary_precision)
                            lst_price = round(li.product_id.lst_price / ratio, monetary_precision)
                            li.write({'price_unit': price_unit,
                                      'lst_price': lst_price})
                        # ... others products in NO WUP LINE:
                        else:
                            if (record.margin_wup_percent < 100):
                                price_unit = round(li.product_id.standard_price / (1 - record.margin_wup_percent / 100) / ratio, monetary_precision)
                                lst_price = round(li.product_id.lst_price / ratio, monetary_precision)
                                li.write(
                                    {'price_unit': price_unit,
                                     'lst_price': lst_price})
                            else:
                                price_unit = round(li.product_id.standard_price * (1 + record.margin_wup_percent / 100) * ratio, monetary_precision)
                                lst_price  = round(li.product_id.lst_price * ratio, monetary_precision)
                                li.write(
                                    {'price_unit': price_unit,
                                     'lst_price': lst_price})

                    # Case Line IS WUP':
                    elif (len(li.wup_line_ids.ids) > 0):
                        sol_price_unit_from_wup = 0
                        for liwup in li.wup_line_ids:
                            # COST Price:
                            if (liwup.fix_price_unit_cost == True):
                                price_unit_cost = liwup.price_unit_cost
                            else:
                                price_unit_cost = round(liwup.product_id.standard_price, monetary_precision)
                            # SALE Price unit (and total):
                            if (liwup.fix_price_unit_sale == True):
                                price_unit = liwup.price_unit
                            elif (liwup.fix_price_unit_sale == False) and (
                                    liwup.product_id.product_tmpl_id.our_service == True) and (
                                    record.discount_type == 'fixed_service_margin_over_cost'):
                                price_unit = record.price_our_service
                            else:
                                if (record.margin_wup_percent < 100):
                                    price_unit = round(price_unit_cost / (1 - record.margin_wup_percent / 100), monetary_precision)
                                else:
                                    price_unit = round(price_unit_cost * (1 + record.margin_wup_percent / 100), monetary_precision)
                            sol_price_unit_from_wup += price_unit * liwup.product_uom_qty
                            liwup.write({'price_unit': price_unit, 'price_unit_cost': price_unit_cost})
                        li.write({'price_unit':sol_price_unit_from_wup, 'discount':0})
            # END CASE FIX_OUR_SERVICES (or not) AND MARGIN_OVER_COST !!
