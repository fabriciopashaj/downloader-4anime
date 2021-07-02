import os

from downloader_4anime import Stream, Status
from downloader_4anime.cacher import AnimeDescriptor

local = os.path.expandvars("$HOME/python/downloader-4anime")
stream = Stream(AnimeDescriptor('Naruto-Shippuden', 'v5.4animu.me', 750),
		 104, 1024 << 4)
print(stream)
stream.on('connect', lambda s: print('Listener 1'))
stream.on('connect', lambda s: print('Listener 2'))
print(stream.proxy)
print(stream.url)
print(stream.download(open('/sdcard/Naruto-Shippuden-104.mp4', 'ab+')))
