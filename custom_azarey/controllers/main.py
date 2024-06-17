
from odoo import _, http
from odoo.http import request
from odoo.http import request, content_disposition


class ProductZippedDownloadController(http.Controller):
    @http.route("/web/products/download_zip", type="http", auth="user")
    def download_zip(self, ids=None, debug=0):
        ids = [] if not ids else ids
        if len(ids) == 0:
            return
        list_ids = map(int, ids.split(","))
        out_file = request.env["product.product"].browse(list_ids)._create_temp_zip()

        content = out_file.getvalue()  # Cf Todo: this is bad
        headers = [
            ('Content-Type', 'zip'),
            ('X-Content-Type-Options', 'nosniff'),
            ('Content-Length', len(content)),
            ('Content-Disposition', content_disposition("product_images"))
        ]
        return request.make_response(content, headers)
