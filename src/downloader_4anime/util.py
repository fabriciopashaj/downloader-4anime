import io, os
from typing import IO, Optional

def length(stream: IO, seekable=True, restore=True) -> int:
	current = stream.tell() - 1
	size = -1
	if seekable and not stream.seekable():
		return -1
	elif stream.seekable():
		size = stream.seek(0, io.SEEK_END)
		if restore:
			stream.seek(current, io.SEEK_SET)
		return size
	else:
		return 0
