from unittest import TestCase, main
from downloader_4anime.events import EventEmitter
import os

class EventEmitterTest(TestCase):
	def setUp(self):
		self.emitter = EventEmitter(['foo', 'bar', 'baz'])
		self.user = os.getenv('USER') or input('user? ')
		self.emitter.on('foo', EventEmitterTest.foo_handler)
		self.emitter.on('hello', EventEmitterTest.hello_handler)
	def test_on(self):
		self.assertNotEqual(self.emitter['foo'], [])
	def test_emit(self):
		self.assertFalse(self.emitter.emit('some unknkown event'))
		self.assertTrue(self.emitter.emit('foo'))
		self.assertTrue(self.emitter.emit('hello'))
		self.assertTrue(self.emitter.emit('hello', self.user))
	
	@staticmethod
	def foo_handler():
		print("foo / bar !")
	@staticmethod
	def hello_handler(name = "World"):
		print("Hello, %s!" % name)

if __name__ == "__main__":
	main()
