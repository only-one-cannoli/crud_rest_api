from sqlite3 import connect
from os.path import exists

from ..defs.settings import Settings


def create_db() -> None:

    connection = connect(Settings.db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        create table widgets (
            uuid text primary key not null,
            name text not null,
            parts int,
            created date not null,
            updated date
        );
    """
    )


def do_sql(query: str) -> None:
    pass


if __name__ == "__main__":
    create_db()
