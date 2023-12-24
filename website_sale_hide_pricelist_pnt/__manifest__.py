# Copyright 2017 Simone Orsi.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Website sale hide pricelists',
    'version': '16.0.1.0.0',
    'author': 'Punt Sistemes',
    'website': 'https://www.puntsistemes.es',
    'license': 'LGPL-3',
    'category': 'Website',
    'summary': 'Pricelist selector hidden on website sale. It will be assigned for the customer but no change option',
    'depends': [
        'website_sale',
    ],
    'data': [
        'data/ir_ui_views.xml',
    ],
    'installable': True,
}
