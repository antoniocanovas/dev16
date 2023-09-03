# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas & PedroGuirao pedro@serincloud.com
##############################################################################

{
    "name": "Account Invoice Retention",
    "version": "14.0.1.0.0",
    "category": "Account",
    "author": "www.serincloud.com",
    "maintainer": "Antoniocanovas",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'account',
    ],
    "data": [
        'views/account_move_views.xml',
        'views/report_invoice_document.xml',
    ],
    "installable": True,
}
