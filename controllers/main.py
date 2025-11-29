import json
import base64
import mimetypes
from odoo import http
from odoo.http import request

class CraftStoriesAPI(http.Controller):

    def _fix_url(self, url, base_url):
        if not url:
            return ""
        if url.startswith("http") or url.startswith("//"):
            return url
        clean_base = base_url.rstrip('/')
        clean_path = url.lstrip('/')
        return f"{clean_base}/{clean_path}"

    def _traverse_and_fix_urls(self, data, base_url):
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['image_url', 'src', 'video_url'] and isinstance(value, str):
                    data[key] = self._fix_url(value, base_url)
                elif isinstance(value, (dict, list)):
                    self._traverse_and_fix_urls(value, base_url)
        elif isinstance(data, list):
            for item in data:
                self._traverse_and_fix_urls(item, base_url)
        return data

    @http.route('/api/craft-stories/content', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_content(self, **kwargs):
        try:
            page = request.env['craft.stories.page'].sudo().search([], limit=1)

            if not page:
                return request.make_response(
                    json.dumps({"error": "No configuration found."}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            raw_data = page.get_page_data()
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            final_data = self._traverse_and_fix_urls(raw_data, base_url)

            response_data = {"data": final_data}
            
            headers = [
                ('Content-Type', 'application/json'),
                ('Access-Control-Allow-Origin', '*'),
                ('Cache-Control', 'public, max-age=60') 
            ]
            
            return request.make_response(
                json.dumps(response_data),
                headers=headers
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
