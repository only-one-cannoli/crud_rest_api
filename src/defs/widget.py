from dataclasses import dataclass
from datetime import datetime
from typing import (
    Optional,
    Tuple,
    Type,
)
from uuid import UUID

from tornado.web import RequestHandler

from .constants import Constants


# pylint: disable=abstract-method
@dataclass
class Widget:

    uuid: Optional[UUID]
    name: str  # len(name) <= 64
    parts: int
    created: datetime
    updated: datetime

    def __post_init__(self):
        # this isn't going to help much except when we construct our API
        # requests in Python

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

    def to_tuple(self):
        return (
            str(self.uuid),
            self.name,
            self.parts,
            self.created.isoformat(),
            self.updated.isoformat(),
        )

    @staticmethod
    def from_tuple(source: Tuple[str, str, int, str, str]):
        return Widget(
            uuid=UUID(source[0]),
            name=source[1],
            parts=source[2],
            created=datetime.fromisoformat(source[3]),
            updated=datetime.fromisoformat(source[4]),
        )


class WidgetHandler(RequestHandler):
    def get(self, _):  # , uuid: Optional[UUID]=None):
        self.write({"widgets": [], "_": _})

    def post(self):  # , widget_data):
        pass

    def delete(self):  # , uuid):
        pass
