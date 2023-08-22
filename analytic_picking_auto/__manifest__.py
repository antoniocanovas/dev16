# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Analityc Picking Auto",
    "summary": "Los productos servidos desde stock no tienen coste por defecto en el proyecto ya que no hay factura de compra, sólo de ingreso."
               "Al asignar plan analítico se cran automáticamente los costes según valor de stock.valuation.layer.",
    "version": "14.0.1.0.0",
    "category": "stock",
    "author": "Pedro Guirao, ",
    "website": "",
    "license": "AGPL-3",
    "depends": [
        "stock_analytic",
        "base_automation",
                ],
    "data": [
#        "data/action_server.xml",
        "views/stock_valuation_layer.xml",
    ],
    "installable": True,
}
