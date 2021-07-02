from unittest import TestCase, main
from downloader_4anime.stream import Stream
from downloader_4anime.cacher import Cacher

class StreamTest(TestCase):
	def setUp(self):
		with Cacher() as cache:
			self.stream = Stream(cache.get_anime_by_id(1), 103)
	def test_properties(self):
		self.assertEqual(self.stream.url,
				'https://4anime.to/naruto-shippuden-episode-103')
		self.assertEqual(self.stream.proxy,
				'https://v5.4animu.me/Naruto-Shippuden/' +
				'Naruto-Shippuden-Episode-103-1080p.mp4')

if __name__ == "__main__":
	main()
