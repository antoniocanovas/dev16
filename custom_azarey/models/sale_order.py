# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        selection_add=[("reservation", "Reservation"), ("sale",)],
        ondelete={"reservation": "set default"},
    )

    risk_remaining_value = fields.Monetary(
        "Risk", store=True, related="partner_id.risk_remaining_value"
    )

    def action_reservation(self):
        self.state = "reservation"

    # Evitar vender el mismo producto a dos tiendas que están juntas y son competencia:
    @api.constrains("write_date")
    def _avoid_product_competency_sale_on_confirm(self):
        for record in self:
            competitor_type = self.env.user.company_id.id
            competitors = (
                self.env["res.partner.relation.all"]
                .search(
                    [
                        ("this_partner_id", "=", record.partner_id.id),
                        ("type_id", "=", competitor_type),
                    ]
                )
                .other_partner_id
            )
            for competitor in competitors:
                for li in record.order_line:
                    sol = self.env["sale.order.line"].search(
                        [
                            ("order_partner_id", "=", competitor.id),
                            ("state", "in", ["reservation", "sale", "done"]),
                            ("product_id", "=", li.product_id.id),
                        ]
                    )
                    if sol.id:
                        mensaje = (
                            "Producto: "
                            + sol[0].product_id.name
                            + " , incompatible por la venta "
                            + sol[0].order_id.name
                            + " al cliente: "
                            + sol[0].order_partner_id.name
                        )
                        raise UserError(mensaje)

    # Considerar el estado RESERVADO para los riesgos financieros:
    def _get_risk_states(self):
        risk_states = super(SaleOrder, self)._get_risk_states()
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
        self.state = "reservation"


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "state",
        "price_reduce_taxinc",
        "qty_delivered",
        "product_uom_qty",
        "qty_invoiced",
    )
    def _compute_risk_amount(self):
        super(SaleOrderLine, self)._compute_risk_amount()

        risk_states = self.env["sale.order"]._get_risk_states()
        for line in self:
            if line.state == "reservation":
                risk_amount = line.price_total * line.product_uom_qty
                line.risk_amount = line.order_id.currency_id._convert(
                    risk_amount,
                    line.company_id.currency_id,
                    line.company_id,
                    line.order_id.date_order
                    and line.order_id.date_order.date()
                    or fields.Date.context_today(self),
                    round=False,
                )
        # for line in self:
        #    if line.state not in risk_states or line.display_type:
        #        line.risk_amount = 0.0
        #        continue
        #    qty = line.product_uom_qty
        #    if line.product_id.invoice_policy == "delivery":
        #        qty = max(qty, line.qty_delivered)
        #    risk_qty = float_round(
        #        qty - line.qty_invoiced, precision_rounding=line.product_uom.rounding
        #    )
        #    # There is no risk if the line hasn't stock moves to deliver
        #    # Added hasattr condition because fails in post-migration compute
        #    if (
        #        risk_qty
        #        and line.qty_delivered_method == "stock_move"
        #        and (hasattr(line, "move_ids"))
        #    ):
        #        if not line.move_ids.filtered(
        #            lambda move: move.state not in ("done", "cancel")
        #        ):
        #            risk_qty = line.qty_to_invoice
        #    if line.state == "reservation":
        #        risk_qty = line.product_uom_qty
        #    if risk_qty == 0.0:
        #        line.risk_amount = 0.0
        #        continue
        #    if line.product_uom_qty:
        #        if line.state == "reservation":
        #            risk_amount = line.price_total * line.product_uom_qty
        #        else:
        # This method has more precision that using price_reduce_taxinc
        #            risk_amount = line.price_total * (risk_qty / line.product_uom_qty)
        #   else:
        #        risk_amount = line.price_reduce_taxinc * risk_qty
        #    line.risk_amount = line.order_id.currency_id._convert(
        #        risk_amount,
        #        line.company_id.currency_id,
        #        line.company_id,
        #        line.order_id.date_order
        #        and line.order_id.date_order.date()
        #        or fields.Date.context_today(self),
        #        round=False,
        #    )
