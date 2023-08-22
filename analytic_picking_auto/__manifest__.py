# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Analityc Picking Auto",
    "summary": "Los productos servidos de stock no tienen coste por defecto en el proyecto ya que no hay factura de compra, sólo de ingreso."
               "¿Cómo distinguir si se va a comprar o no? Por la asignación en línea SM de la cuenta analítica, o un botón para generar estos apuntes.",
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
        "data/action_server.xml",
        "views/stock_valuation_layer.xml",
    ],
    "installable": True,
}
