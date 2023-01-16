import os
from unittest import TestCase
from unittest.mock import patch
import fs


def search_case_sensitive(switch):
    path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_case_sensitive.txt')
    dirlist = fs.get_dirlist(path)
    file = fs.string_file(dirlist[0])
    pattern = 'test'
    cnt_lines = 0
    for line in file:
        result = fs.search(pattern, line, switch)
        if result is not None:
            cnt_lines += 1
    return cnt_lines


class TestFSearch(TestCase):

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

    def test_search_case_sensitive_false(self):
        self.assertEqual(search_case_sensitive(False), 1)

    def test_search_case_sensitive_true(self):
        self.assertEqual(search_case_sensitive(True), 2)

    @patch('os.walk')
    def test_get_dirlist_walk_call(self, mock_system):
        fs.get_dirlist('.')
        mock_system.assert_called()

    @patch('os.path.abspath')
    def test_get_dirlist_path_call(self, mock_system):
        fs.get_dirlist('.')
        mock_system.assert_called()

    def test_get_dirlist_single_file(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_fsearch_input.txt')
        dirlist = fs.get_dirlist(path)
        self.assertEqual(dirlist[0], path)

    def test_get_dirlist_output(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files')
        dirlist = fs.get_dirlist(path)
        self.assertEqual(type(dirlist), list)

    def test_is_hidden_false(self):
        path = '/home/foo/test.txt'
        self.assertFalse(fs.is_hidden(path))

    def test_is_hidden_true(self):
        path = '/home/.foo/test.txt'
        self.assertTrue(fs.is_hidden(path))
