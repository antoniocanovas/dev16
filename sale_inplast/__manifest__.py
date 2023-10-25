{
    'name': 'Custom Inplast Sales',
    'version': '16.0.1.0.0',
    'category': '',
    'description': u"""
Custom Inplast Sales.
Cada cliente sólo tiene posibilidad de ser ofertado en sus productos (ventas, facturas, tarifas, etc).
""",
    'author': 'Serincloud',
    'depends': [
        'contacts',
        'product',
        'sale_management',
        'account_invoice_pricelist',
        'account_invoice_pricelist_sale',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/product_pricelist_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
}
