{
    "name": "Custom Inplast",
    "summary": "Customs Inplast",
    "version": "16.0.1.0.0",
    'category': 'Product, Picking',
    "author": "Punt Sistemes",
    "website": "https://www.puntsistemes.es",
    "Maintainers":[
        "Pedro Guirao",
    ],
    "license": "LGPL-3",
    "depends": [
        "product",
        "stock",
        "report_qweb_pdf_watermark",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_coa.xml",
        "views/menu_views_coa.xml",
        "report/templates.xml",
        "report/ir_action_report.xml",
    ],
    "installable": True,
}
