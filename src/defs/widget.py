from dataclasses import dataclass
from datetime import datetime
from uuid import (
    UUID,
    uuid4,
)
from typing import Type

from tornado.web import RequestHandler

from .constants import Constants


@dataclass
class Widget:

    uuid: UUID
    name: str  # len(name) <= 64
    parts: int
    created: datetime
    updated: datetime

    @staticmethod
    def dummy():
        return Widget(
            uuid=uuid4(),
            name="dummy",
            parts=9999,
            created=Constants.unix_epoch,
            updated=Constants.unix_epoch,
        )


"""
    def from_json(self) -> Type[Widget]:
        pass

    def from_tuple(self) -> Type[Widget]:
        pass
"""


class WidgetHandler(RequestHandler):
    def get(self, _):  # , uuid: Optional[UUID]=None):
        self.write({"widgets": [], "_": _})

    def post(self):  # , widget_data):
        pass

    def delete(self):  # , uuid):
        pass
