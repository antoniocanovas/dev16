# Copyright Serincloud SL - 2023
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Shoes dealer",
    "summary": "Sets, pairs and bom automation.",
    "version": "16.0.1.0.1",
    "category": "stock",
    "author": "Serincloud SL",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "mrp",
        "sale_mrp",
        "project",
        "product_brand",
        "product_variant_sale_price",
        "sale_product_template_tags",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/set_template_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/res_company_views.xml",
        "views/product_attribute_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/product_material_views.xml",
        "views/mrp_bom_views.xml",
    ],
    "installable": True,
}
