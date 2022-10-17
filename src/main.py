from typing import (
    Mapping,
    Type,
)

from tornado.ioloop import IOLoop
from tornado.web import (
    Application,
    RequestHandler,
)

from .db.db import (
    Queries,
    do_sql,
)
from .defs.settings import Settings


class WidgetHandler(RequestHandler):
    def get(self, _):  # , uuid: Optional[UUID]=None):
        self.write({"widgets": [], "_": _})

    def post(self):  # , widget_data):
        pass

    def delete(self):  # , uuid):
        pass


handlers: Mapping[str, Type[WidgetHandler]] = {
    r"/api/v1/widget/([^/]+)?": WidgetHandler,
}

if __name__ == "__main__":
    app = Application(list(handlers.items()))
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
