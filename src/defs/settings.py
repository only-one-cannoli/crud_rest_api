"""
settings.py
Patrick Applegate
18 Oct 2022

Provides settings.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """
    Settings are related to the database and the app itself.
    """

    localhost_port: int = 8888
    database_path: str = "src/db/widgets.db"
    test_database_path: str = "src/db/widgets_test.db"
