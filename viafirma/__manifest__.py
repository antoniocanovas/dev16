# -*- coding: utf-8 -*-
{
    'name': "viafirma",

    'summary': """
        Send documents to be signed on viafirma platform""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ingenieriacloud.com",
    'website': "http://www.ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'contacts',
                'mail',
                ],

    # always loaded
    'data': [
        'data/update_sends.xml',
        'data/ir.model.access.csv',
        'views/views.xml',
        'views/views_menu.xml',
        'views/res_company_views.xml',
        'data/data_notification_signature.xml',
        'wizards/viafirma_wizard_view.xml'
    ],
}
