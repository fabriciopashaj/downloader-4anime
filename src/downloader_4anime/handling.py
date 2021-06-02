from enum import IntEnum
from typing import Union, Optional, Any, Generic
from dataclasses import dataclass

class Status(IntEnum):
	OK = 0
	CONNECTION_REFUSED = 1
	NO_CONNECTION = 2
	DISCONNECTED = 3
	UNKNOWN_ANIME = 4
	SOURCE_NOT_FOUND = 5
	LINKS_NOT_FOUND = 6

@dataclass(frozen=True, order=True)
class Result():
	status: Status
	value: Any = None
	message: Optional[str] = ""
	def __bool__(self):
		return self.status == Status.OK
