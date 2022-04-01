from storage.views import PageNotExists


class MyFramework:
    def __init__(self, urls, middlewares):
        self.urls = urls
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path == '/index/':
            path = '/'

        if path in self.urls:
            view = self.urls[path]
        else:
            view = PageNotExists()
        request = {}

        for middleware in self.middlewares:
            middleware(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


