import os


class SQLParser(object):

    def __init__(self, file_name):
        self.txt = self.open_file(file_name)

    def open_file(self, file_name):
        try:
            with open(file_name) as f:
                return f.read()
        except IOError:
            print "File not found"

    def where_tables(self, where_condition):
        return [i.split('.')[0].strip() for i in where_condition.split('=')]

    def evaluate_where(self, where_condition):
        return set(self.where_tables(where_condition)) <= set(self.tables)

    def determine_join(self, where_condition):
        operator = '(+)'
        if where_condition.endswith(operator):    
            return 'LEFT OUTER JOIN'
        elif operator in where_condition:
            return 'RIGHT OUTER JOIN'
        else:
            return 'INNER JOIN'

    def build_joins(self, where_condition):
        tables = [self.tables[t] for t in self.where_tables(where_condition)]
        join_type = self.determine_join(where_condition)
        return ''.join([tables[0], '\n', join_type, '\n', tables[1], ' ON ', where_condition])

    def build_statement(self):
        joins, where = [], []
        for w in self.where_clause:
            if self.evaluate_where(w):
                joins.append(self.build_joins(w))
            else:
                where.append(w) 
        return ''.join([self.select, 'FROM', '\n', ''.join(joins), '\nWHERE ', 'and'.join(where)])

    @property
    def tables(self):
        from_clause = self.txt[self.txt.index(
            'FROM') + len('FROM'):self.txt.find('WHERE')]
        return {t.replace('\n', '').strip().split(' ')[1]: t.replace('\n', '').strip().split(' ')[0] for t in from_clause.split(',')}

    @property
    def select(self):
        return self.txt[0:self.txt.find('FROM')]

    @property
    def where_clause(self):
        return [w.replace('\n', '').strip() for w in self.txt[self.txt.index('WHERE') + len('WHERE'):].split('AND')]
