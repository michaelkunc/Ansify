import os


class Parser(object):

    def __init__(self, file_name):
        self.text = self.open_file(file_name)

    def open_file(self, file_name):
        try:
            with open(file_name) as f:
                return f.read()
        except IOError:
            print "File not found"
