from unittest import TestCase, main
import sys, os
sys.path.append(os.path.expanduser(os.path.dirname(__file__) + '/../src'))
from downloader_4anime.cacher import Cacher

class CacherTest(TestCase):
	def setUp(self):
		self.cacher = Cacher()
	def test_get_anime_by_name(self):
		with self.cacher as cacher:
			anime = cacher.get_anime_by_name('naruto-shippuden')
			self.assertIsNotNone(anime)
	def test_get_anime_by_id(self):
		anime = self.cacher.get_anime_by_id(1)
		self.assertIsNotNone(anime)

if __name__ == "__main__":
	main()
