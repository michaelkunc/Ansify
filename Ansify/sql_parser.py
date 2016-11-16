import os


class SQLParser(object):

    def __init__(self, file_name):
        self.text = self.open_file(file_name)
        self.from_location = self.substring_location('FROM')
        self.where_location = self.substring_location('WHERE')

    def open_file(self, file_name):
        try:
            with open(file_name) as f:
                return f.read()
        except IOError:
            print "File not found"

    def substring_location(self, substring):
        return (self.text.find(substring), self.text.find(substring) + len(substring))

    def store_where_clause(self):
        where_clause = self.text[self.where_location[1]:]
        return [w.replace('\n', '').strip() for w in where_clause.split('AND')]

    def where_tables(self, where_condition):
        return [i.split('.', 1)[0].strip() for i in where_condition.split('=')]

    def evaluate_where_condition(self, where_condition):
        where_condition_tables = self.where_tables(where_condition)
        return set(where_condition_tables) <= set(self.tables_aliases)

    def determine_join(self, where_condition):
        operator = '(+)'
        if operator in where_condition and where_condition[-len(operator):] == operator:
            return 'LEFT OUTER JOIN'
        elif operator in where_condition:
            return 'RIGHT OUTER JOIN'
        else:
            return 'INNER JOIN'

    def create_joins(self, where_condition):
        first_table = self.tables_aliases[
            self.where_tables(where_condition)[0]]
        second_table = self.tables_aliases[
            self.where_tables(where_condition)[1]]
        join_type = self.determine_join(where_condition)
        return ''.join([first_table, '\n', join_type, '\n', second_table, ' ON ', where_condition])

    def create_select_statement(self):
        return self.text[0:self.from_location[0]]

    def build_select_from(self):
        select = self.create_select_statement()
        joins = [self.create_joins(
            w) for w in self.store_where_clause() if self.evaluate_where_condition(w)]
        where = [w for w in self.store_where_clause(
        ) if not self.evaluate_where_condition(w)]
        return ''.join([select, 'FROM\n', ''.join(joins), self.build_where(where)])

    def build_where(self, where_conditions):
        return '\nWHERE ' + 'and'.join(where_conditions)

    @property
    def tables_aliases(self):
        tables_aliases = self.text[
            self.from_location[1]:self.where_location[0]]
        return {t.replace('\n', '').strip().split(' ')[1]: t.replace('\n', '').strip().split(' ')[0] for t in tables_aliases.split(',')}
