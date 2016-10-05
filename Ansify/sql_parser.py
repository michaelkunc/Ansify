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
        tables_and_aliases = self.store_tables_and_aliases()
        where_condition_tables = self.parse_where_condition_tables(where_condition)
        return set(where_condition_tables) < set(tables_and_aliases)

