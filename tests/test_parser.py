import unittest
from Ansify import sql_parser as p


class SQLParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(SQLParserTest):
        SQLParserTest.ins = p.SQLParser('test_doc.sql')
        SQLParserTest.where = 'PEIA.EXPENDITURE_ITEM_ID = PDIDA.EXPENDITURE_ITEM_ID(+)'

    def test_init(self):
        self.assertEqual(1165, len(SQLParserTest.ins.text))

    # def test_init_error_handling(self):
    #     SQLParserTest.ins = p.SQLParser('file_not_here')
    #     self.assertRaises(IOError, SQLParserTest.ins.text)

    def test_index_of_substring_from(self):
        self.assertEqual((489, 489 + len('FROM')),
                         SQLParserTest.ins.substring_location('FROM'))

    def test_index_of_substring_where(self):
        self.assertEqual((884, 884 + len('WHERE')),
                         SQLParserTest.ins.substring_location('WHERE'))

    def test_store_tables_and_aliases_type(self):
        self.assertEqual(dict, type(
            SQLParserTest.ins.store_tables_and_aliases()))

    def test_store_tables_and_aliases_values(self):
        self.assertEqual('APPS.PA_EXPENDITURE_ITEMS_ALL',
                         SQLParserTest.ins.store_tables_and_aliases()['PEIA'])

    def test_store_where_clause_type(self):
        self.assertEqual(list, type(SQLParserTest.ins.store_where_clause()))

    def test_store_where_clause_values(self):
        self.assertEqual(SQLParserTest.where,
                         SQLParserTest.ins.store_where_clause()[5])

    def test_parse_where_condition_table(self):
        self.assertEqual(['PEIA', 'PDIDA'], SQLParserTest.ins.parse_where_condition_tables(
            'PEIA.EXPENDITURE_ITEM_ID = PDIDA.EXPENDITURE_ITEM_ID(+)'))

    def test_evaluate_where_condition_both_true(self):
        self.assertEqual(
            True, SQLParserTest.ins.evaluate_where_condition(SQLParserTest.where))

    def test_evaluatate_where_condition_one_false(self):
        self.assertEqual(False, SQLParserTest.ins.evaluate_where_condition(
            'PEIA.EXPENDITURE_ITEM_ID = 111232'))

    def test_evaluate_where_condition_both_false(self):
        self.assertEqual(
            False, SQLParserTest.ins.evaluate_where_condition('1=1'))

    def test_determine_join_inner(self):
        self.assertEqual('INNER JOIN', SQLParserTest.ins.determine_join(
            'PEIA.EXPENDITURE_ITEM_ID = PDIDA.EXPENDITURE_ITEM_ID'))

    def test_determine_join_left_outer(self):
        self.assertEqual(
            'LEFT OUTER JOIN', SQLParserTest.ins.determine_join(SQLParserTest.where))

    def test_determine_join_right_out(self):
        self.assertEqual('RIGHT OUTER JOIN', SQLParserTest.ins.determine_join(
            'PEIA.EXPENDITURE_ITEM_ID(+) = PDIDA.EXPENDITURE_ITEM_ID'))

    def test_create_join_statement(self):
        self.assertEqual('APPS.PA_EXPENDITURE_ITEMS_ALL\nLEFT OUTER JOIN\nAPPS.PA_DRAFT_INVOICE_DETAILS_ALL ON PEIA.EXPENDITURE_ITEM_ID = PDIDA.EXPENDITURE_ITEM_ID(+)',
                         SQLParserTest.ins.create_join_statement(SQLParserTest.where))

    def test_create_select_statement(self):
        test_ins = p.SQLParser('short_test_doc.sql')
        self.assertEqual("SELECT DISTINCT \nRCTLGDA.CUSTOMER_TRX_ID AS CUSTOMER_TRX_ID, \nPEIA.EXPENDITURE_ITEM_ID AS PA_TRANS_ID\n\n",
                         test_ins.create_select_statement())

    def test_build_select_from(self):
        test_ins = p.SQLParser('short_test_doc.sql')
        statement = ("SELECT DISTINCT \n"
                     "RCTLGDA.CUSTOMER_TRX_ID AS CUSTOMER_TRX_ID, \n"
                     "PEIA.EXPENDITURE_ITEM_ID AS PA_TRANS_ID\n\n"
                     "FROM\n"
                     "TABLE_1\n"
                     "INNER JOIN\n"
                     "TABLE_2 ON RCTLGDA.EXPENDITURE_ITEM_ID = PEIA.EXPENDITURE_ITEM_ID\n"
                     "WHERE RCTLGDA.TRANSACTION_TYPE = 'CAPITAL'")
        self.assertEqual(statement, test_ins.build_select_from())

    def test_build_where(self):
        test_ins = p.SQLParser('short_test_doc.sql')
        where = ["RCTLGDA.TRANSACTION_TYPE = 'CAPITAL'"]
        self.assertEqual(
            "\nWHERE RCTLGDA.TRANSACTION_TYPE = 'CAPITAL'", test_ins.build_where(where))
