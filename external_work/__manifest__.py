{
    'name': 'External Work',
    'version': '14.0.1.0.1',
    'category': '',
    'description': u"""
External Work app to include services, product and expenses from one place.
""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'sale_management',
        'project',
        'sale_timesheet',
        'hr',
        'hr_expense',
    ],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/default_rules.xml',
        'data/sequence.xml',
        'views/external_work_views.xml',
        'views/menu_views.xml',
        'views/external_work_report.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
