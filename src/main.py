"""
main.py
Patrick Applegate
18 Oct 2022

Contains code to run a Tornado app that provides get, post, patch, and delete
API routes.  Run with pipenv run python -m src.main from the repo's top-level
directory after installing all packages with pipenv install.
"""

from dataclasses import replace
from datetime import (
    datetime,
    timezone,
)
from typing import (
    Dict,
    List,
    Mapping,
    Type,
    cast,
)
from uuid import uuid4

from tornado.ioloop import IOLoop
from tornado.web import (
    Application,
    HTTPError,
    RequestHandler,
)

from .db.db import (
    Queries,
    do_sql,
)
from .db.db_types import DbValues
from .defs.settings import Settings
from .defs.widget import Widget


# pylint: disable=abstract-method
class WidgetHandler(RequestHandler):
    """
    Provides a web-based database interface for widgets.
    """

    def get(self):
        """
        Gets records from the database.  The specific behavior of this function
        depends on the information passed through the query parameters (the
        params argument in requests.get()).  Values for fields other than
        uuid and name are ignored, as are additional values of those fields.

        Returns
        * all records if neither uuid nor name are supplied
        * 0-1 relevant records if a uuid is supplied (uuid is unique)
        * 0-several relevant records if a name is supplied (name is not unique)
        """
        uuid = self.get_query_argument("uuid", None)
        name = self.get_query_argument("name", None)

        if uuid is not None and name is not None:
            raise HTTPError(
                reason="Both uuid and name should not be supplied!"
            )

        if uuid is None and name is None:
            db_widgets = do_sql(
                Queries.select_all,
                None,
                Settings.database_path,
            )

        elif uuid is not None:
            db_widgets = do_sql(
                Queries.select_by_uuid,
                (uuid,),
                Settings.database_path,
            )

        else:
            db_widgets = do_sql(
                Queries.select_by_name,
                (cast(str, name),),
                Settings.database_path,
            )

        self.write({"widgets": to_array(db_widgets)})

    def post(self):
        """
        Inserts a record into the database, given the values supplied in
        the query parameters (the params argument in requests.post()).  params
        should include values for the name and parts fields of a Widget object;
        other fields will be ignored.

        Returns the inserted record.
        """
        new = Widget(
            uuid=uuid4(),
            name=self.get_query_argument("name"),
            parts=int(self.get_query_argument("parts")),
            created=datetime.now(timezone.utc),
            updated=datetime.now(timezone.utc),
        )

        db_widgets = do_sql(
            Queries.insert_record,
            new.to_tuple(),
            Settings.database_path,
        )

        self.write({"widgets": to_array(db_widgets)})

    def patch(self):
        """
        Updates an existing record, given the values supplied in the query
        parameters (the params argument in requests.patch()).  data should
        include a UUID that corresponds to a record in the database, and that
        record will be updated with information from the other fields supplied.
        Only the name and parts fields can be changed by this route; the uuid
        and created fields are fixed once set, and the updated field is changed
        automatically.

        Returns the updated record.
        """
        db_widgets = check_existence(self.get_query_argument("uuid"))

        try:
            old = Widget.from_tuple(db_widgets[0])
        except ValueError as error:
            raise HTTPError(
                reason=f"Malformed record! {db_widgets[0]}"
            ) from error

        params = {
            k: bytes.decode(v[0])
            for k, v in self.request.query_arguments.items()
        }
        to_update = {k: v for k, v in params.items() if k in ("name", "parts")}

        new = replace(old, **to_update, updated=datetime.now(timezone.utc))

        db_widgets = do_sql(
            Queries.update_by_uuid,
            new.to_tuple(),
            Settings.database_path,
        )

        self.write({"widgets": to_array(db_widgets)})

    def delete(self):
        """
        Deletes a record from the database with a UUID supplied in the query
        parameters (the params argument in requests.delete()). Other fields
        supplied through params will be ignored.

        Returns an empty array of records if successful, indicating that the
        deleted record no longer exists in the database.
        """
        uuid = self.get_query_argument("uuid")
        check_existence(uuid)
        db_widgets = do_sql(
            Queries.delete_by_uuid,
            (uuid,),
            Settings.database_path,
        )

        self.write({"widgets": to_array(db_widgets)})


def check_existence(uuid: str) -> List[DbValues]:
    """
    Raises HTTPError if the uuid supplied is not found.
    """
    db_widgets = do_sql(
        Queries.select_by_uuid,
        (uuid,),
        Settings.database_path,
    )
    if len(db_widgets) < 1:
        raise HTTPError(reason="No match for uuid in database!")

    return db_widgets


def to_array(widget_tuples: List[DbValues]) -> List[Dict[str, str]]:
    """
    Convenience function to unpack a list of tuples representing widgets to
    a list of dictionaries.
    """
    array = []
    for w_t in widget_tuples:
        try:
            array.append(Widget.from_tuple(w_t).to_dict())
        except ValueError as error:
            raise HTTPError(reason=f"Malformed record! {w_t}") from error

    return array


handlers: Mapping[str, Type[WidgetHandler]] = {
    "/api/widgets/": WidgetHandler,
}

if __name__ == "__main__":
    app = Application(list(handlers.items()))
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
