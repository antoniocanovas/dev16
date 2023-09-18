# Copyright 2023 Serincloud SL.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Website sale to rental (EE)",
    "summary": "Convert website sales lines to rental sales automatically.",
    "version": "16.0.1.0.0",
    'category': 'Sales',
    "author": "Serincloud SL, ",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "sale_management",
        "website_sale",
        "sale_renting",
                ],
    "data": [
        "views/website_sale_views.xml",
    ],
    "installable": True,
}
