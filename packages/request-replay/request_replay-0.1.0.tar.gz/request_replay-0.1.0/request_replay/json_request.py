import json
import httpx
from .url_request import URLRequest


class JsonRequest(URLRequest):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.body_json = json.loads(self.body_str)

    def request(self, client = None):
        if(client is None):
            client = httpx.Client(http2=True)

        method = self.header_info['method']
        url = self.get_url()

        resp = client.request(
            params=self.header_info['params'],
            method= method,
            url=url,
            headers=self.header_info['headers'],
            json=self.body_json,
        )

        return resp
