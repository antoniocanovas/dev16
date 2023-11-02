# © 2023 Serincloud ( https://www.ingenieriacloud.com )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Power CUPS',
    'version': '16.0.1.0.0',
    'category': '',
    "license": "AGPL-3",
    'website': "https://www.puntsistemes.es",
    'summary': 'Power CUPS',
    'author': 'Punt Sistemes',
    'depends': [
        'mail',
        'contacts',
        'crm',
        'project',
    ],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/power_cups_views.xml',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
}
