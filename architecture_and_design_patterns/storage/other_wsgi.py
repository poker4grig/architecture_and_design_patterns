from my_app import MyFramework


class DebugApp(MyFramework):
    """Дополнительно выводит информацию в консоль"""

    def __init__(self, urls, middlewares):
        self.application = MyFramework(urls, middlewares)
        super().__init__(urls, middlewares)

    def __call__(self, environ, start_response):
        print('DEBUG MODE')
        print(environ)
        return self.application(environ, start_response)


class FakeApp(MyFramework):
    """Фейковое приложение"""
    def __init__(self, urls, middlewares):
        self.application = MyFramework(urls, middlewares)
        super().__init__(urls, middlewares)

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
