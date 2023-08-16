# Copyright 2023 Serincloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Google Fonts",
    "version": "16.0.1.0.0",
    "author": "Serincloud, Odoo Community Association (OCA)",
    "summary": "Collection of all Google fonts",
    "license": "AGPL-3",
    "website": "https://www.ingenieriacloud.com",
    "category": "Report",
    "depends": ["web"],
    "assets": {
        "web.report_assets_common": [
            "google_fonts/static/src/scss/fonts_style.scss",
        ],
        'web.assets_backend': [
            "google_fonts/static/src/scss/fonts_style.scss",
        ],
        'web.assets_frontend': [
            "google_fonts/static/src/scss/fonts_style.scss",
        ],
    },

    "installable": True,
    "maintainers": ["antoniocanovas"],

