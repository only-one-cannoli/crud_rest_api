from dataclasses import (
    dataclass,
    replace,
)
from os.path import exists
from sqlite3 import (
    ProgrammingError,
    connect,
)
from typing import (
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

from ..defs.constants import Constants
from ..defs.settings import Settings
from ..defs.widget import Widget

DbValue = Union[str, int]


@dataclass(frozen=True)
class Queries:

    # NOTE: Trailing comma in SQL gives sqlite3.OperationalError
    create_table: str = f"""
        create table {Settings.table_name} (
            uuid text primary key not null,
            name text not null,
            parts int,
            created text not null,
            updated text not null
        );
    """
    insert_record: str = f"""
        insert into {Settings.table_name} values (?, ?, ?, ?, ?)
    """
    select_all: str = f"select * from {Settings.table_name}"
    select_by_uuid: str = f"select * from {Settings.table_name} where uuid = ?"
    update_by_uuid: str = f"""
        update {Settings.table_name}
        set name = ?, parts = ?, created = ?, updated = ?
        where uuid = ?;
    """
    delete_by_uuid: str = f"delete from {Settings.table_name} where uuid = ?"


def do_sql(
    query: str,
    host_variables: Optional[Tuple[DbValue, ...]] = None,
    database: str = Settings.database_path,
) -> List[Tuple[DbValue, ...]]:
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

        if host_variables is None:
            try:
                result = cursor.execute(query)
            except ProgrammingError as e:
                raise ValueError(
                    "host_variables cannot be None for this query!"
                ) from e
        else:
            result = (
                cursor.execute(query, shifted(host_variables))
                if "update" in query
                else cursor.execute(query, host_variables)
            )

        first_word = query.split()[0]
        if first_word not in ("create", "select"):
            connection.commit()
            return do_sql(
                Queries.select_by_uuid,
                (cast(Tuple[DbValue, ...], host_variables)[0],),
                database=database,
            )

        return result.fetchmany(Settings.to_fetch)


def shifted(host_variables: Tuple[DbValue, ...]):

    lst = list(host_variables)
    return tuple(lst[1:] + [lst[0]])
