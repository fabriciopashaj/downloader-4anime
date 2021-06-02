from .stream import Stream
from .util import format_name, format_source, default_name
from typing import Union
from threading import Thread, Semaphore, Lock
from queue import Queue
import os

class Anime(object):
	def __init__(self, name: str):
		self.name = format_name(name);
		self._url = format_url(self._name)
		self._source = format_source(self._name)
	def download(ep: Union[int, list[int]], path: str = os.curdir,
				name_tmp: str = "%(name)s-Episode-%(ep)i-1080p.mp4",
				chsize: int = None, group_threads: bool = False):
		if name is None:
			name = default_name
		if isinstance(ep, int):
			video = Stream(self.name, ep, chsize or 1024 << 2);
			with open(name_tmp % dict(name=self.name, ep=ep), "ab+") as file:
				video.download(file)
	def spawn(queue: Queue):
		pass
