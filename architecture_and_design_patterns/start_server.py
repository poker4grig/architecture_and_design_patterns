import os

from wsgi_static_middleware import StaticMiddleware
from wsgiref.simple_server import make_server
from tv_series_fw.my_app import MyFramework
from storage.other_wsgi import DebugApp, FakeApp
from storage.views import routes

from storage.middlewares import middlewares


ROOT_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(ROOT_DIR, 'staticfiles')]
application = MyFramework(routes, middlewares)

app_static = StaticMiddleware(application,
                              static_root='staticfiles',
                              static_dirs=STATIC_DIRS)

# application = DebugApp(routes, middlewares)

# application = FakeApp(routes, middlewares)

# with make_server('', 8000, application) as server:
#     print('...running server...')
#     server.serve_forever()

with make_server('', 8000, app_static) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()

