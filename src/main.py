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
        Other (non-UUID, non-name) values in params are ignored.  Additional
        UUIDs and names beyond the first supplied are also ignored.
        """
        # TODO: add pagination

        if params is None:
            db_widgets = do_sql(
                Queries.select_all, None, Settings.database_path
            )
        else:
            params_dict = parse(params)
            uuid = params_dict.get("uuid")
            name = params_dict.get("name")
            neither = uuid is None and name is None
            both = uuid is not None and name is not None
            if neither or both:
                raise ValueError("params must include either uuid or name!")
            elif uuid is not None:
                db_widgets = do_sql(
                    Queries.select_by_uuid, (uuid,), Settings.database_path
                )
            else:
                db_widgets = do_sql(
                    Queries.select_by_name, (name,), Settings.database_path
                )

        self.write({"widgets": to_array(db_widgets)})

    def post(self, params):
        """
        Inserts a record into the database, given the values supplied in
        params.  params should include values for the name and parts fields
        of a Widget object; other fields will be ignored.
        """
        params_dict = parse(params)
        try:
            new_widget = Widget(
                uuid=uuid4(),
                name=params_dict.get("name"),
                parts=int(params_dict.get("parts")),
                created=datetime.now(timezone.utc),
                updated=datetime.now(timezone.utc),
            ).to_tuple()
        except ValueError as e:
            raise ValueError(
                "Bad parameters supplied!"
            ) from e  # TODO: change errors
        db_widgets = do_sql(
            Queries.insert_record, new_widget, Settings.database_path
        )

        self.write({"widgets": to_array(db_widgets)})

    def put(self, params):
        """
        Updates an existing record, given the values supplied in params.
        params should include a UUID that corresponds to a record in the
        database, and that record will be updated with information from the
        other fields supplied through params.
        """
        params_dict = dict(parse_qsl(params))
        if len(params_dict) < 1:
            raise ValueError("No parameters supplied!")
        if "created" in params_dict.keys() or "updated" in params_dict.keys():
            raise ValueError("Don't supply dates created and updated!")

        # widget = Widget.from_dict(

    def delete(self, params):
        """
        Deletes a record from the database with a UUID supplied in params.
        Other fields supplied through params will be ignored.  Sends back an
        empty array of widgets if successful, indicating that the corresponding
        record no longer exists in the database.
        """
        params_dict = parse(params)
        db_widgets = do_sql(
            Queries.delete_by_uuid,
            (params_dict["uuid"],),
            Settings.database_path,
        )

        self.write({"widgets": to_array(db_widgets)})


def parse(param_str: str) -> Dict[str, str]:
    """
    Unpacks a string of params supplied to an API route to a dictionary.
    """
    return dict(parse_qsl(params))


def to_array(widget_tuples: List[DbValues]) -> List[Dict[str, str]]:
    """
    Convenience function to unpack a list of tuples representing widgets to
    a list of dictionaries.
    """

    array = []
    for wt in widget_tuples:
        try:
            array.append(Widget.from_tuple(wt).to_dict())
        except ValueError:
            continue

    return array


handlers: Mapping[str, Type[WidgetHandler]] = {
    r"/api/widgets/([^/]+)?": WidgetHandler,
}

if __name__ == "__main__":
    app = Application(list(handlers.items()), debug=True)  # TODO: remove debug
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
