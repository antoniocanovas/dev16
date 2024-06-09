# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Pablo Archanco Alonso - Aselcis Consulting (http://www.aselcis.com). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": 'Purchase Price Update',
    "version": '1.0',
    "depends": [
        'purchase_discount',
        'account',
    ],
    "author": "Aselcis consulting",
    "category": 'Account',
    "website": "https://www.aselcis.com",
    "description": """
        Update supplierinfo from purchases and incoming invoices 
    """,
    "data": [
        'views/purchase_order_view.xml',
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
