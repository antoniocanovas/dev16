{
    'name': 'Custom Inplast Sales',
    'version': '16.0.1.0.0',
    'category': '',
    'description': u"""
Custom Inplast Sales
""",
    'author': 'Serincloud',
    'depends': [
        'contacts',
        'product',
        'sale_management',
    ],
    'data': [
        'views/res_partner_views.xml',
#        'views/product_pricelist_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
