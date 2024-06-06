from odoo import models, fields, api
import urllib.parse
import urllib.request
import json
import base64


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        record = super(ResPartner, self).create(vals)
        self._send_http_request(record, 'create')
        return record

    def write(self, vals):
        result = super(ResPartner, self).write(vals)
        for record in self:
            self._send_http_request(record, 'write')
        return result

    def unlink(self):
        for record in self:
            self._send_http_request(record, 'unlink')
        result = super(ResPartner, self).unlink()
        return result

    def _send_http_request(self, record, action):

        image_base64 = record.image_1920.decode('utf-8')
        category_ids = record.category_id.ids if record.category_id else []
        data = {
            "id": record.id,
            "name": record.name,
            "image_1920": image_base64,
            "category_id": category_ids,
            "action": action
        }

        url = "http://127.0.0.1:5000/upload"
        headers = {
            'Content-Type': 'application/json',
            'Action': action
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read()
                print(response_body)
        except urllib.error.URLError as e:
            print(e.reason)
