import os


class SQLParser(object):

    def __init__(self, file_name):
        self.text = self.open_file(file_name)
        self.from_location = self.substring_location('FROM')
        self.where_location = self.substring_location('WHERE')
        self.tables_and_aliases = self.store_tables_and_aliases()

    def open_file(self, file_name):
        try:
            with open(file_name) as f:
                return f.read()
        except IOError:
            print "File not found"

    def substring_location(self, substring):
        begin_index = self.text.find(substring)
        end_index = begin_index + len(substring)
        return (begin_index, end_index)

    def store_tables_and_aliases(self):
        tables_and_aliases = self.text[
            self.from_location[1]:self.where_location[0]]
        return {t.replace('\n', '').strip().split(' ')[1]: t.replace('\n', '').strip().split(' ')[0] for t in tables_and_aliases.split(',')}

    def store_where_clause(self):
        where_clause = self.text[self.where_location[1]:]
        return [w.replace('\n', '').strip() for w in where_clause.split('AND')]

    def parse_where_condition_tables(self, where_condition):
        return [i.split('.', 1)[0].strip() for i in where_condition.split('=')]

    def evaluate_where_condition(self, where_condition):
        where_condition_tables = self.parse_where_condition_tables(
            where_condition)
        return set(where_condition_tables) <= set(self.tables_and_aliases)

    def determine_join_type(self, where_condition):
        join_operator = '(+)'
        if join_operator in where_condition and where_condition[-len(join_operator):] == join_operator:
            return 'LEFT OUTER JOIN'
        elif join_operator in where_condition:
            return 'RIGHT OUTER JOIN'
        else:
            return 'INNER JOIN'

    def create_join_statement(self, where_condition):
        first_table = self.tables_and_aliases[
            self.parse_where_condition_tables(where_condition)[0]]
        second_table = self.tables_and_aliases[
            self.parse_where_condition_tables(where_condition)[1]]
        join_type = self.determine_join_type(where_condition)
        return ''.join([first_table, '\n', join_type, '\n', second_table, ' ON ', where_condition])

    def create_select_statement(self):
        return self.text[0:self.from_location[0]]

    def build_select_from(self):
        select = self.create_select_statement()
        temp_var = []
        for w in self.store_where_clause():
            #the evaluation is not correct. Returning false for both conditions
            if self.evaluate_where_condition(w):
                temp_var.append(self.create_join_statement(w))
            else:
                temp_var.append('I DON"T THINK THIS WORKED')
        temp_var = ''.join(temp_var)
        return ''.join([select, temp_var])
