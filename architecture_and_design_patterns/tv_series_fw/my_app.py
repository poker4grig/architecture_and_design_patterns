from storage.views import PageNotExists
import urllib.parse
from tv_series_fw.request_methods import GetMethod, PostMethod
from pprint import pprint


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
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'GET':
            request_params = GetMethod().get_request_params(environ)
            # 127.0.0.1:8000?id=1&category=10  # Пример для ввода
            for key, value in request_params.items():
                value = urllib.parse.unquote_plus(value)
                request_params[key] = value
            request['request_params'] = request_params
            pprint(f'Приняты параметры GET-запроса: {request_params}')

        if method == 'POST':
            data = PostMethod().get_request_params(environ)
            for key, value in data.items():
                value = urllib.parse.unquote_plus(value)
                data[key] = value
            request['data'] = data
            # request['data'] = urllib.parse.unquote_plus(str(data))
            pprint(f'Приняты параметры POST-запроса: {request["data"]}')
            # pprint(f'Вам пришло сообщение от пользователя: '
            #        f'{request["data"]["text"]}')
        for middleware in self.middlewares:
            middleware(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
