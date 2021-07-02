from unittest import TestCase, main
from downloader_4anime.anime import Anime
import os

class AnimeTest(TestCase):
	def setUp(self):
		self.anime1 = Anime('naruto-shippuden')
		self.anime2 = Anime('shingeki-no-kyojin-the-final-season')
		self.anime1.on("download_start", lambda stream, _: print(stream))
	def test__len__(self):
		self.assertEqual(len(self.anime1), 750)
		self.assertEqual(len(self.anime2), 16)
	def test_download(self):
		self.anime1.download(104, os.getenv("SDCARD"), "%(name)s-%(ep)i.mp4",
													1024 << 3);
	def test_spawn(self):
		threads = self.anime1.spawn(list(range(115, 117)), os.getenv("SDCARD"),
												 name_tmp='%(name)s-%(ep)i.mp4')
		self.assertNotEqual(threads.value, [])
		for thread in threads.value:
			thread.join()

if __name__ == "__main__":
	main()
