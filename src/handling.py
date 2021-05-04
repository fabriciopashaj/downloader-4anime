from enum import IntEnum
from typing import Union, Optional, Any
from dataclasses import dataclass

class Status(IntEnum):
    OK = 0
    CONNECTION_REFUSED = 1
    NO_CONNECTION = 2

@dataclass(frozen=True, order=True)
class Result():
    # __slots__ = ["status", "value", "measage"]
    status: Status
    value: Any
    message: Optional[str] = ""
    def __bool__(self):
        return self.status == Status.OK
