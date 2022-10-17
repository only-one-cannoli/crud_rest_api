from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:

    localhost_port: int = 8888
    database_path: str = "src/db/widgets.db"
    test_database_path: str = "src/db/widgets_test.db"
