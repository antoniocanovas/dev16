# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add = [('reservation', "Reservation"), ('sale',)],
                             ondelete={'reservation': 'set default'}
    )

    risk_remaining_value = fields.Monetary('Risk', store=True, related='partner_id.risk_remaining_value')

    # Considerar el estado RESERVADO para los riesgos financieros:
    def _get_risk_states(self):
        super()._get_risk_states(self)
        risk_states.append("reservation")
        return risk_states

    # Copiado de OCA, lo mismo que hace al confirmar pedido, que lo haga en el nuestro de RESERVAR:
    def action_reservation(self):
        if not self.env.context.get("bypass_risk", False):
            for order in self:
                partner = order.partner_invoice_id.commercial_partner_id
                exception_msg = order.evaluate_risk_message(partner)
                if exception_msg:
                    return (
                        self.env["partner.risk.exceeded.wiz"]
                        .create(
                            {
                                "exception_msg": exception_msg,
                                "partner_id": partner.id,
                                "origin_reference": "%s,%s" % ("sale.order", order.id),
                                "continue_method": "action_confirm",
                            }
                        )
                        .action_show()
                    )
        self.state = 'reservation'

    # Evitar vender el mismo producto a dos tiendas que están juntas y son competencia:
    @api.constrains('write_date')
    def _avoid_product_competency_sale_on_confirm(self):
        for record in self:
            competitor_type = self.env.user.company_id.id
            competitors = self.env['res.partner.relation.all'].search(
                [('this_partner_id', '=', record.partner_id.id), ('type_id', '=', competitor_type)]).other_partner_id
            for competitor in competitors:
                for li in record.order_line:
                    sol = self.env['sale.order.line'].search([('order_partner_id', '=', competitor.id),
                                                              ('state', 'in', ['reservation', 'sale', 'done']),
                                                              ('product_id', '=', li.product_id.id)])
                    if sol.id:
                        mensaje = "Producto: " + sol[0].product_id.name + " , incompatible por la venta " + \
                                  sol[0].order_id.name + " al cliente: " + sol[0].order_partner_id.name
                        raise UserError(mensaje)

