import unittest
from Ansify import __main__ as m

class Main(unittest.TestCase):

	def test_main(self):
		self.assertEqual("is this thing on???", m.main())