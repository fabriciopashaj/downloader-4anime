import io
from urllib.request import Request, urlopen
import urllib.error
from .handling import Result, Status
from .util import format_url

function = type(lambda: None)

class Stream(object):
    def __init__(self, name: str, episode: int, chunk_size: int = 1024 << 2):
        self._name = name
        self._ep = episode
        self._chunk_size = chunk_size
        self._req = Request(self.url)
        self._conn = None
        self.__events = {
                'connect': [],
                'end': [],
                'download': [],
                'data': []
        }
    
    def _connect(self):
        try:
            self._conn = urlopen(self._req)
        except ConnectionRefusedError as err:
            return Result(Status.CONNECTION_REFUSED, err,  "Connection was refused")
        except urllib.error.URLError as err:
            return Result(Status.NO_CONNECTION, err, "Couldnt't connect, check your internet")
        else:
            return Result(Status.OK, self._conn)
        
    def connect(self):
        res = self._connect()
        [listener(res) for listener in self.__events['connect']]
        return res
    
    def download(self, outfile: io.TextIOWrapper) -> Result:
        if outfile.closed:
            return Result(Status.FILE_CLOSED, out)
        if self._conn is None:
            st = self.connect()
            if not st:
                outfile.close()
                return st
        with outfile:
            for chunk in self:
                outfile.write(chunk)
        return Result(Status.OK, outfile.name)
    def on(self, event: str, handler: function) -> bool:
        if event not in self.__events.keys() or handler in self.__events[event]:
            return False
        self.__events[event].append(handler)
        
    @property
    def url(self):
        return format_url(self._name, self._ep)
    
    @property
    def video_name(self):
        return "{}-Episode-{}-1080p.mp4".format(self._name, self._ep)
    
    def __repr__(self):
        return "%s('%s', %i)" % (type(self).__name__, self._name, self._ep)
    
    def __call__(self, chunk_size: int = None):
        self._chunk_size = chunk_size if chunk_size is not None else self._chunk_size
        return self
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._conn == None:
            raise StopIteration()
        chunk = self.__conn.read(self._chunk_size)
        if chunk != b'':
            return chunk
        else:
            raise StopIteration()
