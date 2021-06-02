from unittest import TestCase, main
import sys, os
sys.path.append(os.path.expanduser(os.path.dirname(__file__) + '/..'))
from src.cacher import Cacher

class CacherTest(TestCase):
	def setUp(self):
		self.cacher = Cacher()
	def test_get_anime_data(self):
		with self.cacher as cacher:
			anime = cacher.get_anime_data('naruto-shippuden')
			self.assertIsNotNone(anime)

if __name__ == "__main__":
	main()
