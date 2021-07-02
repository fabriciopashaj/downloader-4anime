from urllib.request import Request, urlopen
import io
import urllib.error

from .handling import Result, Status
from .util import length
from .events import EventEmitter
from .cacher import Cacher, AnimeDescriptor

class Stream(EventEmitter):
	def __init__(self, anime: AnimeDescriptor, episode: int,
			chunk_size: int = 1024 << 2):
		self._anime = anime
		self._ep = episode
		self._chunk_size = chunk_size
		self._req = Request(self.proxy, headers={
			'User-Agent': 'Mozilla/5.0',
			# 'Connection': 'Keep-Alive'
		})
		self._conn = None
		EventEmitter.__init__(self, ['connect', 'end', 'download', 'data'])
	
	def _connect(self):
		try:
			self._conn = urlopen(self._req)
		except ConnectionRefusedError as err:
			return Result(Status.CONNECTION_REFUSED, err, "Connection was refused.")
		except urllib.error.URLError as err:
			return Result(Status.NO_CONNECTION, err,
										"Couldnt't connect, check your internet.")
		except ConnectionAbortedError as err:
			return Result(Status.DISCONNECTED, err,
										"A disconnection occured, your internet connection" +
										" may be the cause.")
		except ConnectionError as err:
			return Result(Status.NO_CONNECTION, err,
										"An error occurred while connecting, " +
										"consider trying again.")
		else:
			return Result(Status.OK, self._conn)
		
	def connect(self):
		res = self._connect()
		self.emit('connect', res)
		return res
	
	def download(self, outfile: io.TextIOWrapper) -> Result:
		if outfile.closed:
			result = Result(Status.FILE_CLOSED, outfile)
			self.emit('download', result);
			return result
		if outfile.mode.startswith('r'):
			self._req.add_header('Range', 'bytes=%i-' % length(outfile,
																												 restore=False))
		elif outfile.mode.startswith('a'):
			self._req.add_header('Range', 'bytes=%i-' % outfile.tell())
				
		if self._conn is None or self.__conn.closed:
			st = self.connect()
			if not st:
				outfile.close()
				return st
			else:
				self.__conn = st.value
		bytes_written = 0;
		self.emit("download", Result(Status.OK, outfile))
		for chunk in self:
			self.emit('data', chunk)
			outfile.write(chunk)
			bytes_written += len(chunk)
		if bytes_written >= int(self.__conn.headers['Content-Length']):
			result = Result(Status.OK, outfile)
		else:
			result = Result(Status.DISCONNECTED, outfile,
											"The connection was aborted," +
											"check your internet connection")
		self.emit('end', result)
		return result
		
	@property
	def url(self):
		return 'https://4anime.to/{}-episode-{}'.format(self._anime.name.lower(),
				self._ep)
	
	@property
	def proxy(self):
		return 'https://{}/{}/{}-Episode-{}-1080p.mp4'.format(self._anime.src,
				self._anime.name, self._anime.name, self._ep)
	
	def __repr__(self):
		return "%s('%s', %i)" % (type(self).__name__, self._anime.name, self._ep)
	
	def __call__(self, chunk_size: int = None):
		self._chunk_size = chunk_size if chunk_size is not None else self._chunk_size
		return self
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if self._conn == None:
			raise StopIteration()
		try:
			chunk = self.__conn.read(self._chunk_size)
		except ConnectionAbortedError:
			raise StopIteration()	
		if chunk != b'':
			return chunk
		else:
			raise StopIteration()
