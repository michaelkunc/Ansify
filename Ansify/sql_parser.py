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


    def index_of_substring(self, substring):
    	begin_index = self.text.find(substring)
    	end_index = begin_index + len(substring)
    	return (begin_index, end_index)

