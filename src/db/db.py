from dataclasses import dataclass
from datetime import datetime
from sqlite3 import connect
from os.path import exists
from typing import (Tuple, Optional, Union)

from ..defs.settings import Settings


DbValue = Union[int, str, datetime]

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
    


def do_sql(query: str, host_variables: Optional[Tuple[DbValue, ...]] = None) -> None:
    """
    Executes an SQL query.  If the database file doesn't exist, it will be
    created, together with the widgets table.
    """

    if query != Queries.create_table and not exists(Settings.db_path):
        do_sql(Queries.create_table)

    with connect(Settings.db_path) as connection:
        cursor = connection.cursor()
        if host_variables is None:
            cursor.execute(query)
        else:
            cursor.execute(query, host_variables)


if __name__ == "__main__":
    do_sql(Queries.create_table)
