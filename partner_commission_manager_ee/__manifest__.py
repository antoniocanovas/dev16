# © 2023 Serincloud ( https://www.puntsistemes.es )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Referrer Commission Manager',
    'version': '16.0.1.0.0',
    'category': 'sale_management',
    "license": "AGPL-3",
    'website': "https://puntsistemes.es",
    'summary': 'Add Manager and commission to referrer',
    'author': 'Punt Sistemes',
    'depends': [
        'partner_commission',
        'sale_management',
        'account',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
