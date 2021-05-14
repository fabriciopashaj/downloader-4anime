import io
from urllib.request import Request, urlopen
import urllib.error
import re
from .handling import Result, Status
from .util import format_source, length
from .events import EventEmitter

function = type(lambda: None)

class Stream(EventEmitter):
    def __init__(self, name: str, episode: int, chunk_size: int = 1024 << 2):
        self._name = name
        self._ep = episode
        self._chunk_size = chunk_size
        self._req = Request(self.url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Connection': 'Keep-Alive'
        })
        self._conn = None
        EventEmitter.__init__(self, [
                'connect',
                'end',
                'download',
                'data'
                ])
    
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
        self.emit('connect', res)
        return res
    
    def download(self, outfile: io.TextIOWrapper) -> Result:
        if outfile.closed:
            result = Result(Status.FILE_CLOSED, out)
            self.emit('download', result);
            return result
        if self._conn is None:
            st = self.connect()
            if not st:
                outfile.close()
                return st
            else:
                self.__conn = st.value
        with outfile:
            #if not outfile.mode.startswith(('a', 'w')):
            #    return Result(Status.FILE_READ_ONLY, out, "File is opened in read mode")
            #if "+" in outfile.mode:
            #    self._req.add_header('Range', 'bytes=%i-' % length(outfile))
                
            for chunk in self:
                self.emit('data', chunk)
                outfile.write(chunk)
        result = Result(Status.OK, outfile.name)
        self.emit('end', result)
        return result
        
    @property
    def url(self):
        return format_source(self._name, self._ep)
    
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
