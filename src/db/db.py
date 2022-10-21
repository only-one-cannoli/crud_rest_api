"""
db.py
Patrick Applegate
18 Oct 2022

Provides query text and a key function for executing SQL queries against a
SQLite database.
"""

from dataclasses import dataclass
from os.path import exists
from sqlite3 import (
    ProgrammingError,
    connect,
)
from typing import (
    List,
    Optional,
    Tuple,
    cast,
)

from ..defs.settings import Settings
from .db_types import DbValues


@dataclass(frozen=True)
class Queries:
    """
    Provides the text for SQL commands.
    """

    # NOTE: Trailing comma in SQL gives sqlite3.OperationalError
    create_table: str = """
        create table widgets (
            uuid text primary key not null,
            name text not null,
            parts text not null,
            created text not null,
            updated text not null
        );
    """
    insert_record: str = """
        insert into widgets values (?, ?, ?, ?, ?);
    """
    select_all: str = "select * from widgets;"
    select_by_name: str = "select * from widgets where name = ?;"
    select_by_uuid: str = "select * from widgets where uuid = ?;"
    update_by_uuid: str = """
        update widgets
        set name = ?, parts = ?, created = ?, updated = ?
        where uuid = ?;
    """
    delete_by_uuid: str = "delete from widgets where uuid = ?;"


def do_sql(
    query: str,
    host_variables: Optional[Tuple[str, ...]] = None,
    database: str = Settings.database_path,
) -> List[DbValues]:
    """
    Executes an SQL query.  If the database file doesn't exist, it will be
    created, together with a table.  Recursive -- calls itself if 1) the
    database file doesn't exist, or 2) `query` corresponds to an insert,
    update, or delete operation.
    """

    if query != Queries.create_table and not exists(database):
        do_sql(Queries.create_table, database=database)

    with connect(database) as connection:
        cursor = connection.cursor()

        first_word = query.split()[0]

        if host_variables is None:
            try:
                result = cursor.execute(query)
            except ProgrammingError as error:
                raise ValueError(
                    "host_variables cannot be None for this query!"
                ) from error
        else:
            result = (
                cursor.execute(query, shifted(host_variables))
                if first_word == "update"
                else cursor.execute(query, host_variables)
            )

        if first_word not in ("create", "select"):
            connection.commit()
            return do_sql(
                Queries.select_by_uuid,
                (cast(Tuple[str, ...], host_variables)[0],),
                database=database,
            )

        return result.fetchall()


def shifted(host_variables: Tuple[str, ...]):
    """
    Moves the uuid from the first position to the last within host_variables
    if we're doing an update.
    """

    lst = list(host_variables)
    return tuple(lst[1:] + [lst[0]])
