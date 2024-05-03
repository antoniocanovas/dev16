{
    'name': "partner credentials",
    'summary': """
        Nuevo modelo para documentar usuario y contraseña de aplicaciones.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'contacts',
        'hr',
    ],
    'data': [
        'views/partner_credential_views.xml',
        'views/menu_views.xml',
        'views/res_partner_views.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/default_rules.xml',
    ],
    'installable': True,
    'application': True,
}
