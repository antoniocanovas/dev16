# Copyright 2023 Serincloud SL.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Custom Azarey",
    "summary": "Customs Azarey",
    "version": "16.0.1.0.0",
    'category': 'Sales',
    "author": "Serincloud SL",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "product",
        "mail",
        "contacts",
        "sale_management",
        "partner_multi_relation",
        "mrp",
        "l10n_es_partner",
        "stock",
        "product_variant_sale_price",
    ],
    "data": [
        "views/product_attribute_views.xml",
        "views/product_pricelist_views.xml",
        "views/product_views.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
