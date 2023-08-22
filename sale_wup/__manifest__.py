{
    'name': 'WUP',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'project',
        'account',
        'sale_margin',
        'product_brand',
        'hr',
        'base_automation',
        'analytic_picking_auto',
    ],
    'data': [
        'data/server_action.xml',
        'data/automated_action.xml',
        'security/ir.model.access.csv',
        'views/model_views.xml',
        'views/menu_views.xml',
        'views/sale_order_views.xml',
        'views/product_views.xml',
        'views/project_task.xml',
        'views/wup_saleline_wizard_views.xml',
    ],
    'installable': True,
}
