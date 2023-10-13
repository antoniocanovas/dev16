# © 2023 Serincloud ( https://www.ingenieriacloud.com )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Fleet extended',
    'version': '16.0.1.0.0',
    'category': 'fleet',
    "license": "AGPL-3",
    'website': "https://ingenieriacloud.com",
    'summary': 'Add fields for estimated km and real consumed, and additional cost.',
    'author': 'Punt Sistemes',
    'depends': [
        'fleet',
        'account_fleet',
    ],
    'data': [
        'views/fleet_vehicle_log_contract_views.xml',
    ],
    'installable': True,
    'application': False,
}
