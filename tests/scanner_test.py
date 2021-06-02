from unittest import TestCase, main
import sys, os
sys.path.append(os.path.expanduser(os.path.dirname(__file__) + '/..'))
from src.scanner import Scanner

class ScannerTest(TestCase):
	def setUp(self):
		self.scanner = Scanner("https://4anime.to/naruto-shippuden-episode-1")
	def test_source(self):
		status = self.scanner.get_source()
		self.assertEqual(status.value,
										 "https://v5.4animu.me/Naruto-Shippuden/Naruto-Shippuden-Episode-1-1080p.mp4")
	def test_links(self):
		status = self.scanner.get_links()
		self.assertTrue(bool(status))
		self.assertNotEqual(status.value, [])

if __name__ == "__main__":
	main()
