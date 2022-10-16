from dataclasses import dataclass
from sqlite3 import connect
from os.path import exists

from ..defs.settings import Settings


@dataclass(frozen=True)
class Queries:

    create_table: str = """
        create table widgets (
            uuid text primary key not null,
            name text not null,
            parts int,
            created date not null,
            updated date
        );
    """


def do_sql(query: str, create_if_missing: bool=True) -> None:
    """
    Executes an SQL query.  if the database file doesn't exist, it will be
    created, together with the widgets table.
    """

    if create_if_missing and not exists(Settings.db_path):
        do_sql(Queries.create_table, False)

    with connect(Settings.db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(query)


if __name__ == "__main__":
    do_sql(Queries.create_table, False)
