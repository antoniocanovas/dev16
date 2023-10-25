# © 2023 Serincloud ( https://www.ingenieriacloud.com )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Custom Inmopolt',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    "license": "AGPL-3",
    'website': "https://ingenieriacloud.com",
    'summary': 'Inmopolt Customs',
    'author': 'Serincloud',
    'depends': [
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
