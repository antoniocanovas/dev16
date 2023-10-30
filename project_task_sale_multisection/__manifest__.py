{
    'name': 'Project Task Sale Multisection',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
     Añade a la tarea la sección del pedido de venta.
""",
    'author': 'Serincloud',
    'depends': [
        'sale_order_multisection',
        'sale_timesheet',
    ],
    'data': [
        'views/model_views.xml',
    ],
    'installable': True,
}
