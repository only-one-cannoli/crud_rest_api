"""
test_db.py
Patrick Applegate
18 Oct 2022

Provides tests for the database connection and the relevant SQL commands.
"""

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
    """
    Tests and fixtures to test the database connection.
    """

    @pytest.fixture
    def remove_test_database(self):
        """
        Removes the test database if it exists.
        """
        if exists(Settings.test_database_path):
            remove(Settings.test_database_path)

    @pytest.fixture
    def widgets(self):
        """
        Sets up a dictionary with tuple values representing widgets.
        """
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
        """
        Gives a tuple with the keys of widget-tuples that we'll try to insert.
        """
        return ("original", "another")

    def test_insert(self, remove_test_database, widgets, to_insert):
        """
        Check that insertion works.
        """
        # pylint: disable-next=pointless-statement
        remove_test_database
        for key in to_insert:
            result = do_sql(
                Queries.insert_record,
                widgets[key],
                database=Settings.test_database_path,
            )
            assert result == [widgets[key]]

    def test_insert_duplicate_uuid(self, widgets):
        """
        Ensure that any given UUID is unique.
        """
        with pytest.raises(IntegrityError):
            do_sql(
                Queries.insert_record,
                widgets["original"],
                database=Settings.test_database_path,
            )

    def test_select_all(self, widgets, to_insert):
        """
        Check that we can get back all the records.
        """
        result = do_sql(
            Queries.select_all,
            database=Settings.test_database_path,
        )
        assert result == [widgets[k] for k in to_insert]

    def test_select_by_name(self, widgets, to_insert):
        """
        Check that we can select records by name.  Note that we get more than
        one result here; the name field isn't assumed to be unique.
        """
        result = do_sql(
            Queries.select_by_name,
            ("dummy",),
            database=Settings.test_database_path,
        )
        assert result == [widgets[key] for key in to_insert]

    def test_select_by_uuid(self, widgets, to_insert):
        """
        Check that we can select records by UUID.  Here, we get only one
        record, as the sqlite database ensures that we can't have two records
        with the same UUID.
        """
        for key in to_insert:
            uuid = widgets[key][0]
            result = do_sql(
                Queries.select_by_uuid,
                (uuid,),
                database=Settings.test_database_path,
            )
            assert result == [widgets[key]]

    def test_update_by_uuid(self, widgets):
        """
        Check that updating given the UUID of an existing record works.
        """
        result = do_sql(
            Queries.update_by_uuid,
            widgets["updated"],
            database=Settings.test_database_path,
        )
        assert result == [widgets["updated"]]

    def test_delete_by_uuid(self, widgets):
        """
        Check that we can delete records given a UUID.
        """
        uuid = widgets["another"][0]
        result = do_sql(
            Queries.delete_by_uuid,
            (uuid,),
            database=Settings.test_database_path,
        )
        assert result == []

    def test_post_delete(self, widgets):
        """
        After all of the above, we should have only the updated record left.
        """
        result = do_sql(
            Queries.select_all,
            database=Settings.test_database_path,
        )
        assert result == [widgets["updated"]]
