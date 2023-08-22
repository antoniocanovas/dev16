{
    'name': 'Sale Order Konery',
    'version': '16.0.1.0.0',
    'category': '',
    'description': u"""
Sale Order Konery
""",
    'author': 'Serincloud',
    'depends': [
        'sale_margin',
    ],
    'data': [
        'data/server_actions.xml',
        'views/sale_order_margin_wizard_views.xml',
        'views/sale_order_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
