import unittest
from Ansify import sql_parser as p


class SQLParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(SQLParserTest):
        SQLParserTest.ins = p.SQLParser('test_doc.sql')

    def test_init(self):
        self.assertEqual(1167, len(SQLParserTest.ins.text))

    # def test_init_error_handling(self):
    #     SQLParserTest.ins = p.SQLParser('file_not_here')
    #     self.assertRaises(IOError, SQLParserTest.ins.text)

    def test_index_of_substring_from(self):
        self.assertEqual((491, 491 + len('FROM')),
                         SQLParserTest.ins.substring_location('FROM'))

    def test_index_of_substring_where(self):
        self.assertEqual((886, 886 + len('WHERE')),
                         SQLParserTest.ins.substring_location('WHERE'))

    def test_store_tables_and_aliases_type(self):
        self.assertEqual(dict, type(SQLParserTest.ins.store_tables_and_aliases()))

    def test_store_tables_and_aliases_values(self):
        self.assertEqual('APPS.PA_EXPENDITURE_ITEMS_ALL', SQLParserTest.ins.store_tables_and_aliases()['PEIA'])

    def test_store_where_clause_type(self):
        self.assertEqual(list, type(SQLParserTest.ins.store_where_clause()))

    def test_store_where_clause_values(self):
        self.assertEqual('PEIA.EXPENDITURE_ITEM_ID = PDIDA.EXPENDITURE_ITEM_ID(+)', SQLParserTest.ins.store_where_clause()[5])

    def test_evaluate_where_condition(self):
        self.assertEqual(True, SQLParserTest.ins.evaluate_where_condition('PEIA.EXPENDITURE_ITEM_ID = PDIDA.EXPENDITURE_ITEM_ID(+)'))
