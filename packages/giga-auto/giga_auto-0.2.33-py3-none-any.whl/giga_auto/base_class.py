from giga_auto.request import RequestBase


class ApiBase(RequestBase):
    def __init__(self, **env):
        self.set_env(**env)
        super().__init__(self.host, env.get('expect_code', 200))

    def set_env(self, **env):
        self.host = env.get('host', getattr(self, 'host', None))
        self.headers = env.get('headers', getattr(self, 'headers', {}))

    def set_headers(self, headers):
        self.headers = headers
