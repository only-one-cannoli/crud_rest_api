"""
widget.py
Patrick Applegate
18 Oct 2022

Provides the Widget dataclass.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import (
    Dict,
    Optional,
    cast,
)
from uuid import UUID

from ..db.db_types import DbValues
from .constants import Constants


@dataclass
class Widget:
    """
    This class provides a convenient container for widget-related information.
    We pass this information through this class using the from_* and to_*
    methods so that we can check that the information satisfies some
    constraints.  A sqlite database won't do that for us.
    """

    uuid: Optional[UUID]
    name: str  # len(name) <= 64
    parts: int
    created: datetime
    updated: datetime

    def __post_init__(self):

        if len(self.name) > 64:
            raise ValueError("Widget.name cannot exceed 64 characters!")

    @staticmethod
    def dummy():
        """
        Gives an obviously fake Widget object for testing purposes.
        """
        return Widget(
            uuid=Constants.zeroes_uuid,
            name="dummy",
            parts=9999,
            created=Constants.unix_epoch,
            updated=Constants.unix_epoch,
        )

    def to_tuple(self) -> DbValues:
        """
        Converts a Widget to a tuple of strings.
        """
        return (
            str(self.uuid),
            str(self.name),
            str(self.parts),
            self.created.isoformat(),
            self.updated.isoformat(),
        )

    @staticmethod
    def from_tuple(source: DbValues):
        """
        Attempts to construct a Widget from a tuple of strings.  Should throw
        ValueError if this process fails.
        """
        return Widget(
            uuid=UUID(source[0]),
            name=str(source[1]),
            parts=int(source[2]),
            created=datetime.fromisoformat(source[3]),
            updated=datetime.fromisoformat(source[4]),
        )

    def to_dict(self) -> Dict[str, str]:
        """
        Constructs a dictionary with string values from a Widget.
        """
        return {
            "uuid": str(self.uuid),
            "name": str(self.name),
            "parts": str(self.parts),
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
        }

    @staticmethod
    def from_dict(source: Dict[str, str]):
        """
        Constructs a Widget from a dictionary; throws errors on failure.
        """
        return Widget(
            uuid=UUID(cast(Optional[str], source.get("uuid"))),
            name=str(source["name"]),
            parts=int(source["parts"]),
            created=datetime.fromisoformat(source["created"]),
            updated=datetime.fromisoformat(source["updated"]),
        )
