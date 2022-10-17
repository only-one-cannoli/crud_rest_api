from dataclasses import dataclass
from types import MappingProxyType
from typing import (
    Mapping,
    Type,
)

from .widget import WidgetHandler


@dataclass(frozen=True)
class Settings:

    handlers: Mapping[str, Type[WidgetHandler]] = MappingProxyType(
        {
            r"/api/v1/widget/([^/]+)?": WidgetHandler,
        }
    )
    localhost_port: int = 8888
    database_path: str = "src/db/widgets.db"
    test_database_path: str = "src/db/test_widgets.db"
    table_name: str = "widgets"
    to_fetch: int = 3
