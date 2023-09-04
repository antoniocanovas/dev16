{
    'name': 'Invoice from origin',
    'version': '16.0.1.0.0',
    'category': 'Account',
    'description': 'Permite facturación de obras en origen desde una factura generada desde el pedido de venta, teniendo en cuenta los conceptos ya facturados, según solicitan constructuras.',
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'account',
        'analytic',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'data/server_action.xml',
        'views/templates.xml',
        'views/report.xml',
    ],
    'installable':True,
}
