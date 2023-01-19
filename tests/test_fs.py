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

    def test_search_regular_expressions(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_case_sensitive.txt')
        dirlist = fs.get_dirlist(path)
        file = fs.string_file(dirlist[0])
        pattern = '[1-5]'
        expected_output_line_1 = b'test\x1b[91m1\x1b[0m\x1b[91m2\x1b[0m\x1b[91m3\x1b[0m'.decode('utf-8')
        expected_output_line_2 = b'TEST\x1b[91m4\x1b[0m\x1b[91m5\x1b[0m6'.decode('utf-8')
        result_1 = fs.search(pattern, file[0])
        result_2 = fs.search(pattern, file[1])
        self.assertEqual(result_1, expected_output_line_1)
        self.assertEqual(result_2, expected_output_line_2)

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

    def test_get_dirlist_exclude(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files')
        dirlist = fs.get_dirlist(path, extensions='txt')
        self.assertEqual(len(dirlist), 1)

    def test_get_dirlist_level(self):
        path = os.path.join(os.path.dirname(__file__), '.')
        lv = 1
        dirlist = fs.get_dirlist(path, level=lv)
        # length should be equal of all files in tests/ directory
        self.assertEqual(len(dirlist), 1)

    def test_get_dirlist_hidden(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files')
        filename = path + '/.test_hidden.txt'
        dir_list = fs.get_dirlist(path, hidden=True)
        self.assertTrue(filename in dir_list)

    def test_is_hidden_false(self):
        path = '/home/foo/test.txt'
        self.assertFalse(fs.is_hidden(path))

    def test_is_hidden_true(self):
        path = '/home/.foo/test.txt'
        self.assertTrue(fs.is_hidden(path))

    def test_get_path_level(self):
        root_path = '/home/test'
        child_path_1 = '/home/test/test1/test2/test3'
        child_path_2 = '/home/test/test1/test2/test3/test4/test5/test6/test7/test8/test9/test10'
        result_1 = fs.get_path_level(root_path, child_path_1)
        result_2 = fs.get_path_level(root_path, child_path_2)
        self.assertEqual(result_1, 3)
        self.assertEqual(result_2, 10)
