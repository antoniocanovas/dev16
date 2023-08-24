# © 2023 Serincloud ( https://www.ingenieriacloud.com )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account financial risk contracts',
    'version': '16.0.1.0.0',
    'category': '',
    "license": "AGPL-3",
    'website': "https://www.ingenieriacloud.com",
    'summary': 'Risk contracts history and details',
    'author': 'Serincloud',
    'depends': [
        'account',
        'account_financial_risk',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/risk_contract_views.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
