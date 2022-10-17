from dataclasses import dataclass
from types import MappingProxyType
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


@dataclass(frozen=True)
class Settings:

    handlers: Mapping[str, Type[WidgetHandler]] = MappingProxyType(
        {
            r"/api/v1/widget/([^/]+)?": WidgetHandler,
        }
    )
    localhost_port: int = 8888
    database_path: str = "src/db/widgets.db"
    test_database_path: str = "src/db/test_widgets.db"


class WidgetHandler(RequestHandler):
    def get(self, _):  # , uuid: Optional[UUID]=None):
        widgets = do_sql(
            Queries.select_all
        )  # , None, Settings.test_database_path)  # TODO: change test database to actual database
        self.write({"widgets": widgets, "_": _})

    def post(self):  # , widget_data):
        pass

    def delete(self):  # , uuid):
        pass


if __name__ == "__main__":
    app = Application(list(Settings.handlers.items()))
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
