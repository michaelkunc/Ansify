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
        return {t.replace('\n','').strip().split(' ')[1]: t.replace('\n','').strip().split(' ')[0] for t in tables_and_aliases.split(',')}

    def store_where_clause(self):
        where_clause = self.text[self.where_location[1]:]
        return [w.replace('\n','').strip() for w in where_clause.split('AND')]

