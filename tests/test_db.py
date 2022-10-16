from dataclasses import replace
from os import remove
from os.path import exists

import pytest

from src.db.db import (
    Queries,
    do_sql,
)
from src.defs.constants import Constants
from src.defs.settings import Settings
from src.defs.widget import Widget


class TestDatabase:
    @pytest.fixture
    def remove_test_database(self):
        if exists(Settings.test_database_path):
            remove(Settings.test_database_path)

    @pytest.fixture
    def widget_tuple(self):
        return Widget.dummy().to_tuple()

    @pytest.fixture
    def updated_widget_tuple(self, widget_tuple):
        return replace(
            Widget.from_tuple(widget_tuple),
            name="fake",
            updated=Constants.end_day,
        ).to_tuple()

    def test_insert(self, remove_test_database, widget_tuple):
        result = do_sql(
            Queries.insert_record,
            widget_tuple,
            database=Settings.test_database_path,
        )
        assert result == [widget_tuple]

    def test_select_all(self, widget_tuple):
        result = do_sql(
            Queries.select_all,
            database=Settings.test_database_path,
        )
        assert result == [widget_tuple]

    def test_select_by_uuid(self, widget_tuple):
        result = do_sql(
            Queries.select_by_uuid,
            (widget_tuple[0],),
            database=Settings.test_database_path,
        )
        assert result == [widget_tuple]

    def test_update_by_uuid(self, updated_widget_tuple):
        result = do_sql(
            Queries.update_by_uuid,
            updated_widget_tuple,
            database=Settings.test_database_path,
        )
        assert result == [updated_widget_tuple]

    def test_delete_by_uuid(self, widget_tuple):
        result = do_sql(
            Queries.delete_by_uuid,
            (widget_tuple[0],),
            database=Settings.test_database_path,
        )
        assert result == []
