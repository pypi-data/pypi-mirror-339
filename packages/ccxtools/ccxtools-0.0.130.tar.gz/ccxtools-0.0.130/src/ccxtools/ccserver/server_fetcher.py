import requests


class ServerFetcher:

    def __init__(self, domain, token, program):
        self.domain = domain
        self.token = token
        self.program = program

        self.session = ResponseCheckingSession()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def _is_v2_endpoint(self, url: str) -> bool:
        return url.startswith(f'{self.domain}/v2/')

    def post_login(self) -> None:
        self.session.post(
            f'{self.domain}/v2/auth/login',
            json={'token': self.token}
        )

    def request_get(self, url, params=None):
        if params is None:
            params = {}
        
        if self._is_v2_endpoint(url):
            return self.session.get(url, params=params)
        else:
            response = requests.get(url, params=params)
            if not 200 <= response.status_code < 300:
                raise HttpError(response)
            return response

    def request_post(self, url, data):
        if self._is_v2_endpoint(url):
            try:
                return self.session.post(url, json=data)
            except HttpError as e:
                if e.status_code == 401:
                    self.post_login()
                    return self.session.post(url, json=data)
        else:
            response = requests.post(url, json=data, headers={
                'Authorization': f'Token {self.token}',
                'Content-Type': 'application/json',
            })
            if not 200 <= response.status_code < 300:
                raise HttpError(response)
            return response

    def post_log_error(self, exception, traceback):
        return self.request_post(f'{self.domain}/logs/errors/', {
            'program': self.program,
            'exception': exception,
            'traceback': traceback,
        })


class ResponseCheckingSession(requests.Session):
    
    def request(self, method, url, *args, **kwargs):
        response = super().request(method, url, *args, **kwargs)
        if not 200 <= response.status_code < 300:
            raise HttpError(response)
        return response


class HttpError(requests.exceptions.RequestException):

    def __init__(self, response: requests.Response):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text
        self.url = response.url
        self.method = response.request.method
        self.headers = response.headers
        super().__init__(f"HTTP {response.status_code} {response.reason}: {response.text}")