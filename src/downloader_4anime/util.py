import io, os
from typing import IO, Optional
# TODO: Make doc
def format_source(name: str, ep: Optional[int] = None) -> str:
	"""
	Formats an anime's source url by its name (and its episode if specified)
	params:
		name: str ->					The name of the anime
		ep: Optional[int] ->	The episode of the anime, if None the url
														will have only the anime's url
	return:
		Returns the formated url
	example:
		>>> from downloader_4anime.util import format_source
		>>> print(format_source("Naruto-Shippuden"))
		https://v5.4animu.me/Naruto-Shippuden/
		>>> print(format_source("Naruto-Shippuden", 86))
		https://v5.4animu.me/Naruto-Shippuden/Naruto-Shippuden-Episode-86-1080p.mp4
	"""
	return f'https://v5.4animu.me/{name}/{name}-Episode-{ep}-1080p.mp4' if ep is not None\
			else f'https://v5.4animu.me/{name}/'
def format_name(name: str) -> str:
	return map(str.capitalize, name.replace(' ', '-').title())
def format_url(name: str, ep: int = None) -> str:
	return f'https://4anime.to/{name}/{name}-Episode-{ep}-1080p.mp4' if ep is not None\
			else f'https//4anime.to/{name}/'

def default_name(name: str, ep: int) -> str:
	return '{}-Episode-{}-1080p.mp4'.format(name, ep)

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

def unimplemented(func=None,
		template="Function '%(func_name)s' is unimplemented"):
	def _wraper(*args, **kwargs):
		if os.getenv("PYTHON_ENV") in ("dev", "test"):
			print(f"[warning]: {template}" % dict(func_name=func.__name__))
	if func is None:
		return lambda func: _wraper
	else:
		return _wraper
