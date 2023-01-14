import os
import unittest
import fs


class TestFSearch(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_string_file.txt')
        self.output = fs.string_file(self.path)

    def test_string_file_type(self):
        self.assertEqual(type(self.output), list)

    def test_string_file_size(self):
        self.assertEqual(len(self.output), 7)

    def test_string_file_printable_characters(self):
        printable_characters = '0123456789 abcdefghijklmnopqrstuvwxyzABCDEFGHIJ' \
                               'KLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_printable_characters.txt')
        output = fs.string_file(path)[0]
        self.assertEqual(output, printable_characters)
