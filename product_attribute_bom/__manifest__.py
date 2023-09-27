# Copyright Serincloud SL - 2023
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Product Set from attributes",
    "summary": "Set Product bom creation from set template variants.",
    "version": "16.0.1.0.0",
    "category": "stock",
    "author": "Serincloud SL",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "mrp",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/set_template_views.xml",
        "views/product_views.xml",
        "views/product_attribute_views.xml",
        #        "data/action_server.xml",
    ],
    "installable": True,
}
