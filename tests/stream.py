import sys, os
sys.path.append(os.path.expandvars('.'))

from src import Stream, Status

local = os.path.expandvars("$HOME/python/downloader-4anime")
stream = Stream('Naruto-Shippuden', 85)
print(stream)
stream.on('connect', lambda s: print('Listener 1'))
stream.on('connect', lambda s: print('Listener 2'))

print(stream.download(open(local+'/videos/' + stream.video_name, 'wb')))
