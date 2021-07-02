from .stream import Stream
from .cacher import Cacher
from .events import EventEmitter
from .handling import Result, Status
from typing import Union
from threading import Thread #, Semaphore, Lock
# from queue import Queue
import os, time

class Anime(EventEmitter):
	def __init__(self, name: str):
		EventEmitter.__init__(self, ['spawn', 'download_start',
																 'download_end', 'receive'])
		with Cacher() as cache:
			if not (descriptor := cache.get_anime_by_name(name)):
				raise NameError("Anime '%s' is not registered in the database" % name)
			else:
				self.descriptor = descriptor
	def spawn(self, episodes: Union[int, list[int]], path: str = os.curdir,
						name_tmp: str = "%(name)s-Episode-%(ep)i-1080p.mp4",
						chsize: int = None, block: bool = False) -> list[Thread]:
		if isinstance(episodes, int):
			episodes = [episodes]
		chsize = chsize or 1024 << 2
		threads = []
		for ep in episodes:
			thread = Thread(target=self.download, args=(ep, path, name_tmp, chsize))
			thread.start()
			self.emit('spawn', thread)
			threads.append(thread)
			time.sleep(0.5)
		if block:
			list(map(Thread.join, threads))
		return Result(Status.OK, threads, "Anime(s) dwnloaded suceessfilly")
	def download(self, ep: int, directory: str, template: str, chsize: int):
		stream = Stream(self.descriptor, ep, chsize)
		path = '%s/%s' % (directory,
													template % dict(name=self.descriptor.name, ep=ep))
		stream.on('download',
							lambda result: self.emit('download_start', stream, result))
		stream.on('end',
							lambda result: self.emit('download_end', stream, result))
		stream.on('data', lambda data: self.emit('receive', stream, data))
		file = open(path, 'ab+' if os.path.isfile(path) else 'wb+')
		if result := stream.download(file):
			result.value.close()
		else:
			print("Failed downloading '%s' episode %i" % (stream._anime.name,
																										stream._ep))
	def __len__(self):
		return self.descriptor.episode_count
	def __repr__(self):
		return repr(self.descriptor)
	def __str__(self):
		return self.descriptor.name
