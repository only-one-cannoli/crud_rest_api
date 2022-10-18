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
    def get(self, params: Optional[str] = None):
        """
        Gets records from the database.  The specific behavior of this function
        depends on params.
        If params is None, all records are retrieved.
        If params contains a UUID, only the relevant record is retrieved.
        If params contains a name, only the relevant records are retrieved.
        Other (non-UUID, non-name) values in params are ignored.
        """

        if params is None:
            db_widgets = do_sql(Queries.select_all, None, database)
        else:
            params_dict = dict(parse_qsl(params))
            uuid = params_dict.get("uuid")
            name = params_dict.get("name")
            neither = uuid is None and name is None
            both = uuid is not None and name is not None
            if neither or both:
                raise ValueError("params must include either uuid or name!")
            elif uuid is not None:
                db_widgets = do_sql(Queries.select_by_uuid, (uuid,), database)
            else:
                db_widgets = do_sql(Queries.select_by_name, (name,), database)

        widgets = []
        for widget in db_widgets:
            widgets.append(Widget.from_tuple(widget).to_dict())
            try:
                widgets.append(Widget.from_tuple(widget).to_dict())
            except ValueError:
                continue

        self.write({"widgets": widgets})

    def post(self, params):
        """
        Inserts a record into the database or updates an existing record,
        depending on the contents of params.
        If params does not include a UUID, one is generated, and the resulting
        widget is inserted into the database.
        If params includes a UUID that corresponds to a record in the database,
        the record is updated with information from the other fields.
        """
        pass

    def delete(self, params):
        """
        Deletes a record from the database with a UUID supplied in params.
        """
        pass


handlers: Mapping[str, Type[WidgetHandler]] = {
    r"/api/widgets/([^/]+)?": WidgetHandler,
}

if __name__ == "__main__":
    app = Application(list(handlers.items()), debug=True)  # TODO: remove debug
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
