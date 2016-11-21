import os


class SQLParser(object):

    def __init__(self, file_name):
        self.text = self.open_file(file_name)

    def open_file(self, file_name):
        try:
            with open(file_name) as f:
                return f.read()
        except IOError:
            print "File not found"


    def where_tables(self, where_condition):
        return [i.split('.', 1)[0].strip() for i in where_condition.split('=')]

    def evaluate_where(self, where_condition):
        return set(self.where_tables(where_condition)) <= set(self.tables)

    def determine_join(self, where_condition):
        operator = '(+)'
        if operator in where_condition and where_condition[-len(operator):] == operator:
            return 'LEFT OUTER JOIN'
        elif operator in where_condition:
            return 'RIGHT OUTER JOIN'
        else:
            return 'INNER JOIN'

    def build_joins(self, where_condition):
        table_1 = self.tables[self.where_tables(where_condition)[0]]
        table_2 = self.tables[self.where_tables(where_condition)[1]]
        join_type = self.determine_join(where_condition)
        return ''.join([table_1, '\n', join_type, '\n', table_2, ' ON ', where_condition])

    def build_statement(self):
        joins = [self.build_joins(w)
                 for w in self.where_clause if self.evaluate_where(w)]
        where = [w for w in self.where_clause if not self.evaluate_where(w)]
        return ''.join([self.select, 'FROM', '\n', ''.join(joins), '\nWHERE ', 'and'.join(where)])

    @property
    def tables(self):
        from_clause = self.text[self.text.index(
            'FROM') + len('FROM'):self.text.find('WHERE')]
        return {t.replace('\n', '').strip().split(' ')[1]: t.replace('\n', '').strip().split(' ')[0] for t in from_clause.split(',')}

    @property
    def select(self):
        return self.text[0:self.text.find('FROM')]

    @property
    def where_clause(self):
        return [w.replace('\n', '').strip() for w in self.text[self.text.index('WHERE') + len('WHERE'):].split('AND')]
