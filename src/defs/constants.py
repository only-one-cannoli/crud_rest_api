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
    zeroes_uuid: UUID = UUID("00000000-0000-0000-0000-000000000000")
    ones_uuid: UUID = UUID("11111111-1111-1111-1111-111111111111")


if __name__ == "__main__":
    print(Constants.unix_epoch, Constants.zeroes_uuid)
