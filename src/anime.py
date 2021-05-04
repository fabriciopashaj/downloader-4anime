from .stream import Stream
from .util import format_name

class Anime(object):
    def __init__(self, name: str):
        self.name = format_name(name);
        self._url = format_url(self._name)
        self._source = format_source(self._name)
