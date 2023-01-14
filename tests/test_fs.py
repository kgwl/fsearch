import os
import unittest
import fs


class TestFSearch(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_fsearch_input.txt')
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

    def test_string_file_non_printable_characters(self):
        string1 = 'test'
        string2 = '123'
        path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_non_printable_characters.txt')
        output = fs.string_file(path)
        self.assertEqual(output[0], string1)
        self.assertEqual(output[1], string2)

    def test_search_output_colored(self):
        pattern = 'faucibus mi quis dui'
        excepted_result = 'Phasellus ' \
                          + '\033[91m' + 'faucibus mi quis dui' \
                          + '\033[0m' + ' ultrices tristique. ' \
                                        'Morbi efficitur leo felis, sit ' \
                                        'amet fringilla ante iaculis ut.'
        result = ''
        for line in self.output:
            searched_phrase = fs.search(pattern, line)
            if searched_phrase is not None:
                result = searched_phrase

        self.assertEqual(result, excepted_result)
