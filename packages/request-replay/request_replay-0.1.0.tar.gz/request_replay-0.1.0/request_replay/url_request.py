import httpx


class URLRequest():
    @staticmethod
    def extract_params(url: str):
        params = {}
        if '?' in url:
            url, param_str = url.split('?', 1)
            for param in param_str.split('&'):
                key, value = param.split('=')
                params[key] = value
        return url, params


    @staticmethod
    def parse_header(header_str: str):
        header_list = header_str.split('\n')
        req_attr_str = header_list[0].split(' ')

        req_path = req_attr_str[1]
        req_path, params = URLRequest.extract_params(req_path)


        header_dict = {}

        for line in header_list[1:]:
        
            key, value = line.split(': ', 1)
            if(key == 'Content-Length'):
                continue
            header_dict[key] = value
        

        return {
            'method': req_attr_str[0],
            'req_path': req_path,
            'params': params,
            'protocol': req_attr_str[2],
            'headers': header_dict
        }
    
    def __init__(self, file_path):
        self.request_str = open(file_path, 'r', encoding='utf-8').read()
        header_str, body_str = self.request_str.split('\n\n', 1)

        self.header_info = self.parse_header(header_str)
        self.body_str = body_str

    def get_url(self, overrided_scheme = None):
        host = self.header_info['headers']['Host']
        scheme = 'https'
        if overrided_scheme is not None:
            scheme = overrided_scheme
            
        return f'{scheme}://{host}{self.header_info["req_path"]}'

    def request(self, client = None, override_scheme = None):
        if(client is None):
            client = httpx.Client(http2=True)

        method = self.header_info['method']
        url = self.get_url(override_scheme)

        resp = client.request(
            params=self.header_info['params'],
            method= method,
            url=url,
            headers=self.header_info['headers'],
        )

        return resp
