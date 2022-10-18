from dataclasses import dataclass
from datetime import datetime
from typing import (
    Dict,
    Optional,
    Tuple,
    Type,
    cast,
)
from uuid import UUID

from tornado.web import RequestHandler

from ..db.db_types import DbValues
from .constants import Constants


@dataclass
class Widget:

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
        return Widget(
            uuid=Constants.zeroes_uuid,
            name="dummy",
            parts=9999,
            created=Constants.unix_epoch,
            updated=Constants.unix_epoch,
        )

    def to_tuple(self) -> DbValues:
        return (
            str(self.uuid),
            self.name,
            str(self.parts),
            self.created.isoformat(),
            self.updated.isoformat(),
        )

    @staticmethod
    def from_tuple(source: DbValues):
        return Widget(
            uuid=UUID(source[0]),
            name=source[1],
            parts=int(source[2]),
            created=datetime.fromisoformat(source[3]),
            updated=datetime.fromisoformat(source[4]),
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "parts": str(self.parts),
            "created": self.created.isoformat(),
            "updated": self.created.isoformat(),
        }

    @staticmethod
    def from_dict(source: Dict[str, str]):
        return Widget(
            uuid=UUID(cast(Optional[str], source.get("uuid"))),
            name=source["name"],
            parts=int(source["parts"]),
            created=datetime.fromisoformat(source["created"]),
            updated=datetime.fromisoformat(source["updated"]),
        )
