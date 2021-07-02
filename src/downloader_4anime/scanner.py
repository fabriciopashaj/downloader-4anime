from dataclasses import dataclass, field
from urllib.request import urlopen, Request
from typing import Dict, Union, List
import re
from .handling import Result, Status

Cache = Dict[str, Union[str, List[str]]]
source_finder = re.compile(
		r'src="(https://\w+(?:\.\w+){2}/[^/]+/[^\.]+\.mp4)',
		re.IGNORECASE)
episode_link_finder = re.compile(
		r' href="(https://4anime.to/[a-z-]+episode-\d+/?[^"]+")',
		re.IGNORECASE)
@dataclass
class Scanner(object):
	url: str
	_content = None
	cache: Cache = field(default_factory=lambda: dict())
	def get_source(self):
		if "source" in self.cache:
			return Result(Status.OK, self.cache["source"])
		else:
			return self.extract_source()
	def get_nams(self):
		if "source" in self.cache:
			return Result(Status.OK, self.cache["source"].split("/")[2])
		else:
			return self.extract_name()
	def extract_name(self):
		if source := self.extract_source():
			return Result(Status.OK, source.value.split("/")[2])
		else:
			return source
	def get_links(self):
		if "links" in self.cache:
			return Result(Status.OK, self.cache["links"])
		else:
			return self.extract_links()
	def pull_content(self):
		connection = urlopen(Request(self.url, headers={
			'User-Agent': 'Mozilla/5.0',
			'Range': 'bytes=32768-57344'
		}))
		if connection.code == 404:
			return Result(Status.UNKNOWN_ANIME, connection,
										"The url you provided points to a non existent anime."
										"Try copying and pasting the url again")
		self._content = connection.read().decode("utf-8")
		connection.close()
		return Result(Status.OK)
	def extract_source(self):
		if self._content is None and not (result := self.pull_content()):
			return result
		sources = source_finder.findall(self._content)
		if len(sources) == 0:
			return Result(Status.SOURCE_NOT_FOUND, self._content,
										"The page doesn't have an anime source")
		source = sources[0]
		self.cache["source"] = source
		return Result(Status.OK, source)
	def extract_links(self):
		if self._content is None and not (result := self.pull_content()):
			return result
		links = episode_link_finder.findall(self._content)
		if len(links) == 0:
			return Result(Status.LINKS_NOT_FOUND, self._content,
										"The page doesn't have any matching links")
		links = list(set(map(lambda link: link.split('?')[0], links)))
		self.cache["links"] = links
		return Result(Status.OK, links)
