import unittest
from Ansify import sql_parser as p


class SQLParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(SQLParserTest):
        SQLParserTest.instance = p.SQLParser('test_doc.sql')

    def test_init(self):
        self.assertEqual(1167, len(SQLParserTest.instance.text))

    def test_init_error_handling(self):
    	SQLParserTest.instance = p.SQLParser('file_not_here')
        self.assertRaises(IOError, SQLParserTest.instance.text)

    def test_find_index_of_substring(self):
    	self.assertEqual((491,491 + len('FROM')), SQLParserTest.instance.find_index_of_substring('FROM'))

