from wsgiref.simple_server import make_server
from tv_series_fw.my_app import MyFramework
from storage.urls import urls
from storage.middlewares import middlewares


application = MyFramework(urls, middlewares)
with make_server('', 8000, application) as server:
    print('...running server...')
    server.serve_forever()
