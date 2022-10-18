from dataclasses import replace
from os import remove
from os.path import exists
from sqlite3 import IntegrityError

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
    def widgets(self):
        dummy = Widget.dummy()
        return {
            "original": dummy.to_tuple(),
            "another": replace(dummy, uuid=Constants.ones_uuid).to_tuple(),
            "updated": replace(
                dummy, parts=7777, updated=Constants.end_day
            ).to_tuple(),
        }

    @pytest.fixture
    def to_insert(self):
        return ("original", "another")

    def test_insert(self, remove_test_database, widgets, to_insert):
        # pylint: disable-next=pointless-statement
        remove_test_database
        for key in to_insert:
            result = do_sql(
                Queries.insert_record,
                widgets[key],
                database=Settings.test_database_path,
            )
            assert result == [widgets[key]]

    def test_select_all(self, widgets, to_insert):
        result = do_sql(
            Queries.select_all,
            database=Settings.test_database_path,
        )
        assert result == [widgets[k] for k in to_insert]

    def test_select_by_name(self, widgets, to_insert):
        result = do_sql(
            Queries.select_by_name,
            ("dummy",),
            database=Settings.test_database_path,
        )
        assert result == [widgets[key] for key in to_insert]

    def test_select_by_uuid(self, widgets, to_insert):
        for key in to_insert:
            uuid = widgets[key][0]
            result = do_sql(
                Queries.select_by_uuid,
                (uuid,),
                database=Settings.test_database_path,
            )
            assert result == [widgets[key]]

    def test_update_by_uuid(self, widgets):
        result = do_sql(
            Queries.update_by_uuid,
            widgets["updated"],
            database=Settings.test_database_path,
        )
        assert result == [widgets["updated"]]

    def test_delete_by_uuid(self, widgets):
        uuid = widgets["another"][0]
        result = do_sql(
            Queries.delete_by_uuid,
            (uuid,),
            database=Settings.test_database_path,
        )
        assert result == []

    def test_post_delete(self, widgets):
        result = do_sql(
            Queries.select_all,
            database=Settings.test_database_path,
        )
        assert result == [widgets["updated"]]

    def test_insert_duplicate_uuid(self, widgets):
        with pytest.raises(IntegrityError):
            do_sql(
                Queries.insert_record,
                widgets["original"],
                database=Settings.test_database_path,
            )

    def test_insert_bad_data(self):
        """
        Unfortunately, sqlite doesn't seem to do any type checking at all;
        "brown" isn't coercible to an integer in Python, but sqlite accepts
        it happily in the `parts` field.  The `strict` keyword doesn't seem
        to be available in this version of sqlite, either.
        """
        bad_widget = ("the", "quick", "brown", "fox", "jumped")
        result = do_sql(
            Queries.insert_record,
            bad_widget,
            database=Settings.test_database_path,
        )
        assert result == [bad_widget]
