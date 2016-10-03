import unittest
from Ansify import sql_parser as p


class SQLParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(SQLParserTest):
        SQLParserTest.instance = p.SQLParser('test_doc.sql')

    def test_init(self):
        self.assertEqual(1167, len(SQLParserTest.instance.text))

    # def test_init_error_handling(self):
    #     SQLParserTest.instance = p.SQLParser('file_not_here')
    #     self.assertRaises(IOError, SQLParserTest.instance.text)

    def test_index_of_substring_from(self):
        self.assertEqual((491, 491 + len('FROM')),
                         SQLParserTest.instance.substring_location('FROM'))

    def test_index_of_substring_where(self):
        self.assertEqual((886, 886 + len('WHERE')),
                         SQLParserTest.instance.substring_location('WHERE'))

    def test_store_tables_and_aliases_type(self):
        self.assertEqual(list, type(SQLParserTest.instance.store_tables_and_aliases()))
