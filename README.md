# downloader-4anime
Automated anime downloader for downloading anime from the [*4anime.to*](https://4anime.to/) website
-------------------------------------------------------------------------------
# WARNING: The library doesn't work anymore since the website was taken down.
-------------------------------------------------------------------------------
## Install
```bash
pip install downloader-4anime
```
## NOTICE
If you don't understand programming related topics, terms and coding in general or if you don't understand what is written below, I suggest you to clik [here](NON_CODERS.md).
## Usage
This library can be imported into a python project or script as any other library. CLI support comming soon.
The library has multiple classes that do and handle different things.
### Event driven design
The downloading system adopts an event driven behavior. If you know NodeJS, it will be easy for you to adopt to it.
#### EventEmmitter
If you know NodeJS' **EventEmmitter** class. you can skip below, it is somehow the same.
When you initialise an **EventEmmitter** object, it receives only one argument, an array of strings with the names of the events that will be registered first. Is probably useless. Just a way to show someone who looks at the code which events he should be listening for.
More than one listener can be attached to a single event. They will get called in the same order as registered.
Example:
```python
from downloader_4anime import EventEmmitter
import time

bus = EventEmitter(["foo", "bar"])
# Passing a lambda as a callback
bus.on("foo", lambda: print("foo event fired"))
# Pasing a def
def __bar1():
	print("bar event fired")
	time.sleep(1)
bus.on("bar", __bar1)
# Emiting events
bus.emit("foo")
bus.emit("bar")

```
### Handling different cases with Result and Status
The library handles different behaviours using `Result`s and `Status`es instead of eagerly throwing exceptions. The **Result** class has three fields: status, value and message. The status field is an enum of **Status**. The value field is whatever is returned with the result. The message field is an optional string describing what happened or failed and why.
The result can be checked directly using an *if* statement due to the use of `__bool__` overload. If the status is not Status.OK, it results to False.
Check src/downloader\_4anime/handling.py for a list of **Status**es.
### Downloading
#### Anime
The main downloading class is the **Anime** class. With it you can download multiple episodes in parallel using it's *spawn* method.
Example:
```python
from downloader_4anime import Anime
anime = Anime('naruto-shippuden')
# download a single episode
anime.download(103, '%(name)s-%(ep)i.mp4', 1024 << 4)
# download multiple episodes in parallel
anime.spawn([103, 104, 105], '/home/<user>/anime', '%(name)s-%(ep)i.mp4') # or 'C:\\Users\\<user>\\anime' for windows
# Episode count of the anime
len(anime)
```
**NOTE:** If the anime is not registered in the database, a `NameError` will be thrown. See [below](#cacher) for more info.
#### Stream
The class that is used for stream-downloading the videos. This class is used by the **Anime** class. The **Stream** class can download only a single anime. You can use this class if you want to have higher control over your downloads, but if you just want to download them, use **Anime**.
Example:
```python
from downloader_4anime import Stream, Cacher
with Cacher() as cache:
	anime_data = cacher.get_anime_by_name('naruto-shippuden')
	stream = Stream(anime_data, 104) # Can have a 3rd parameter, the size of the chunk thaf will be fetched from the server.
	if not (status := stream.connect()): # Will return a Result if the connection was successful or not
		print(status.message)
		exit(1)
	with open("%s-%i.mp4" % (anime_data.name, 104), 'wb+') as video:
		# When using 'ab+' or 'rb+', it will try to continue the download.
		stream.download(video)
	print(stream.url) # Will print https://4anime.to/naruto-shippuden-episode-104
	print(stream.proxy) # Will print the proxy server url https://v5.4animu.me/Naruto-Shippuden/Naruto-Shippuden-Episode-104-1080p.mp4
	print(stream) # Will print Stream('Naruto-Shippuden', 104)
	stream(1024 * 16) # Or stream.__call__(1024 * 16), sets the streaming chunk size, useful when doing a for...in loop without changing the size in another line
```
### Scanning and caching
#### Scanner
The **Scanner** class scans the webpage of the anime, from the url you provide and extracts the useful urls.
Example:
```python
from downloader_4anime import Scanner
# Initialise with the url of a random episode of some anime
scanner = Scanner('https://4anime.to/shingeki-no-kyojin-final-season-episode-6')
# Each of the methods below return a result.
# If anything goes as expected it should print:
# Result(<Status.OK: 0>, 'Shingeki-no-Kyojin-Final-Season', '')
# Gets the name of the anime used in the url below
print(scanner.get_name())
# Gets the url where the video is streamed from
print(scanner.get_source())
# Gets the urls of each episode of the anime
print(scanner.get_links())
```
#### Cacher
The **Cacher** class caches the data that is extracted using the **Scanner** class to a SQLite database located at `$HOME/anime.db` for faster loading.
The **Cacher** class has a setup method. It should **NEVER** be invoked by the user.
Example:
```python
from downloader_4anime import Cacher, Scanner
scanner = Scanner('https://4anime.to/shingeki-no-kyojin-final-season-episode-6')
cacher = Cacher()
# We got to check for the result of each of them
if not (name := scanner.get_name()):
	cacher.close()
	raise Error(name.message)
else:
	name = name.value
if not (source := scanner.get_source()):
	cacher.close()
	raise Error(source.message)
else:
	source = source.value
if not (links := scanner.get_links()):
	cacher.close()
	raise Error(links.message)
else:
	links = links.value
# We register the anime to the database
cacher.register_anime(name, source, len(links))
# We update the anime if it already exists
cacher.update_anime(name, source=source, ep_count=len(links))

# We get the descriptor of an anime by its name
# The descriptor is a namedtuple named AnimeDescriptor that can be imported from the library.
print(cacher.get_anime_by_name("naruto-shippuden"))
# Or by its id in the database's table if you know it
print(cacher.get_anime_by_id(1)) # Its still gonna print the same thing as above, Naruto Shippuden is automatically registered as the first when the database is created.
# Prints how many animes are registered
print(len(cacher))
cacher.close()
```

