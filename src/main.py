from json import loads
from typing import (
    Mapping,
    Optional,
    Type,
)
from urllib.parse import parse_qsl

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
from .defs.widget import Widget


class WidgetHandler(RequestHandler):
    def get(
        self, params: Optional[str] = None, database=Settings.database_path
    ):

        if params is None:
            db_widgets = do_sql(Queries.select_all, None, database)
        else:
            uuid = dict(parse_qsl(params))["uuid"]
            db_widgets = do_sql(Queries.select_by_uuid, (uuid,), database)

        widgets = []
        for widget in db_widgets:
            widgets.append(Widget.from_tuple(widget).to_dict())
            try:
                widgets.append(Widget.from_tuple(widget).to_dict())
            except ValueError:
                continue

        self.write({"widgets": widgets})

    def post(self):  # , widget_data):
        pass

    def delete(self):  # , uuid):
        pass


handlers: Mapping[str, Type[WidgetHandler]] = {
    r"/api/widgets/([^/]+)?": WidgetHandler,
}

if __name__ == "__main__":
    app = Application(list(handlers.items()), debug=True)  # TODO: remove debug
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
