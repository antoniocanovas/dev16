{
    'name': "partner credentials",
    'summary': """
        Nuevo modelo para documentar usuario y contraseña de aplicaciones.
        Lee con atención las indicaciones de la dependencia field_encryption. Añadir en conf:
        server_wide_modules = web,field_encryption y
        encryption_key='YOUR_KEY'
        """,
    'author': "Antonio Cánovas",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '16.0.1.0.0',
    'depends': [
        'contacts',
        'hr',
        'field_encryption',
    ],
    'data': [
        'security/user_groups.xml',
        'views/partner_credential_views.xml',
        'views/partner_credential_category_views.xml',
        'views/menu_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'data/default_rules.xml',
    ],
    'installable': True,
    'application': True,
}
