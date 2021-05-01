import io
from urllib.request import Request, urlopen
import urllib.error
from .handling import Result, Status
from .util import format_url

#TODO: Complete class
class Stream(object):
    def __init__(self, name: str, episode: int):
        self._name = name
        self._ep = episode
        self._req = Request(self.url)
        self._conn = None
    def connect(self):
        try:
            self._conn = urlopen(self._req)
        except ConnectionRefusedError as err:
            return Result(Status.CONNECTION_REFUSED, err,  "Connection was refused")
        except urllib.error.URLError as err:
            return Result(Status.NO_CONNECTION, err, "Couldnt't coonect, check your internet")
        else:
            return Result(Status.OK, self._conn)
    @property
    def url(self):
        return format_url(self._name, self._ep)
    def __repr__(self):
        return "%s([%s] %i)" % (type(self).__name__, self._name, self._ep)
