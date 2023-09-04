{
    'name': 'External Work Sale Type',
    'version': '14.0.1.0.1',
    'category': '',
    'description': u"""
External Work integration with OCA sale_order_type
""",
    'author': 'Serincloud',
    'depends': [
        'external_work',
        'sale_order_type',
    ],
    'data': [
        'views/external_work_views.xml',
    ],
    'installable': True,
}
