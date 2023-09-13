# © 2023 Serincloud ( https://www.ingenieriacloud.com )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'FSM Task planning',
    'version': '16.0.1.0.0',
    'category': '',
    "license": "AGPL-3",
    'website': "https://ingenieriacloud.com",
    'summary': 'FSM Task Planning',
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'sale_subscription',
        'project',
    ],
    'data': [
        'views/sale_order_template_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
