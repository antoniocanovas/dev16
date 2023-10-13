# © 2023 Serincloud ( https://www.puntsistemes.es )
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Fleet extended',
    'version': '16.0.1.0.1',
    'category': 'fleet',
    "license": "AGPL-3",
    'website': "https://puntsistemes.es",
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
