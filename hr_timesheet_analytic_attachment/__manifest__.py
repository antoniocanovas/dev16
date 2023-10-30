# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas antonio.canovas@serincloud.com
##############################################################################

{
    "name": "Hr timesheet attachment in Analytic line",
    "version": "14.0.1.0.0",
    "category": "Account",
    "author": "www.serincloud.com",
    "maintainer": "Antonio Cánovas",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    'description': u"""
    Timesheet work sheet attachments in analytic forms, when is a time record (employee assigned).
    """,
    "depends": [
        'hr_timesheet_work',
    ],
    "data": [
        'views/account_analytic_line_views.xml'
    ],
    "installable": True,
}
