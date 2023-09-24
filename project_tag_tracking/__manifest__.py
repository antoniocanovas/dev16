# -*- coding: utf-8 -*-

{
    'name': 'Project and task tags traking',
    'version': '16.0.1.0.0',
    'category': 'Project/Project',
    'summary': "Use Tags to follow your workflow",
    'description': "Every change in task tags are tracked to chatter, only with difference not all tags previous. "
                   "It's recommended when there are a lot of tags",
    'author': 'Serincloud',
    'company': 'Serincloud',
    'maintainer': 'Serincloud',
    'website': 'https://www.ingenieriacloud.com',
    'depends': [
        'project',
        'base_automation',
    ],
    'data': [
        'data/automatic_actions.xml',
    ],
    'assets': {},

    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
