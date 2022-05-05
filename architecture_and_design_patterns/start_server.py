from wsgiref.simple_server import make_server
from tv_series_fw.my_app import MyFramework
from storage.other_wsgi import DebugApp, FakeApp
from storage.views import routes

from storage.middlewares import middlewares


application = MyFramework(routes, middlewares)

# application = DebugApp(routes, middlewares)

# application = FakeApp(routes, middlewares)

with make_server('', 8000, application) as server:
    print('...running server...')
    server.serve_forever()

