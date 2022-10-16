from dataclasses import dataclass
from datetime import (
    datetime,
    timezone,
)
from uuid import UUID


@dataclass(frozen=True)
class Constants:
    unix_epoch: datetime = datetime(
        1970, 1, 1, microsecond=0, tzinfo=timezone.utc
    )
    end_day: datetime = datetime(
        1997, 9, 1, microsecond=0, tzinfo=timezone.utc
    )
    null_uuid: UUID = UUID("00000000-0000-0000-0000-000000000000")
    range_uuid: UUID = UUID("12345678-9101-1121-3141-516171819202")


if __name__ == "__main__":
    print(Constants.unix_epoch, Constants.null_uuid)
