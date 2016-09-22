import unittest
from Ansify import parser as p


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(ParserTest):
        ParserTest.instance = p.Parser('test_doc.sql')

    def test_init(self):
        self.assertEqual(1167, len(ParserTest.instance.text))

    def test_init_error_handling(self):
    	ParserTest.instance = p.Parser('file_not_here')
        self.assertRaises(IOError, ParserTest.instance.text)
