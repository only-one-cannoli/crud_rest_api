from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Constants:
    unix_epoch: datetime = datetime(1970, 1, 1)

if __name__ == "__main__":
    print(Constants.unix_epoch)
