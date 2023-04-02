import os
from unittest import TestCase
from unittest.mock import patch
import fs
import pandas as pd
import argparse
from io import StringIO


def search_case_sensitive(switch):
    path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_case_sensitive.txt')
    dirlist = fs.get_filelist(path)
    file = fs.string_file(dirlist[0])
    pattern = 'test'
    cnt_lines = 0
    for line in file:
        result = fs.search(pattern=pattern, line=line, case_sensitive=switch)
        if result is not None:
            cnt_lines += 1
    return cnt_lines


class TestFSearch(TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_fsearch_input.txt')
        self.output = fs.string_file(self.path)
        self.path = 'test_input_files/test_simple_analyse.txt'
        self.dir_list = fs.get_filelist(self.path)
        self.base_dir = self.dir_list[0][0: len(self.dir_list) - len(self.path) - 1]
        self.dir_name = self.dir_list[0]

        data = [[self.dir_name, self.path, 4, 17]]
        self.data_frame = pd.DataFrame(data, columns=['Full_Path', 'Path', 'Lines', 'Size'])

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
        self.assertEqual(search_case_sensitive(False), 2)

    def test_search_case_sensitive_true(self):
        self.assertEqual(search_case_sensitive(True), 1)

    def test_search_regular_expressions(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_case_sensitive.txt')
        dirlist = fs.get_filelist(path)
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
        fs.get_filelist('.')
        mock_system.assert_called()

    @patch('os.path.abspath')
    def test_get_dirlist_path_call(self, mock_system):
        fs.get_filelist('.')
        mock_system.assert_called()

    def test_get_dirlist_single_file(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files/test_fsearch_input.txt')
        dirlist = fs.get_filelist(path)
        self.assertEqual(dirlist[0], path)

    def test_get_dirlist_output(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files')
        dirlist = fs.get_filelist(path)
        self.assertEqual(type(dirlist), list)

    def test_get_dirlist_exclude(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files')
        dirlist = fs.get_filelist(path, extensions='txt')
        self.assertEqual(len(dirlist), 1)

    def test_get_dirlist_level(self):
        path = os.path.join(os.path.dirname(__file__), '.')
        lv = 1
        dirlist = fs.get_filelist(path, level=lv)
        # length should be equal of all files in tests/ directory
        self.assertEqual(len(dirlist), 1)

    def test_get_dirlist_hidden(self):
        path = os.path.join(os.path.dirname(__file__), 'test_input_files')
        filename = path + '/.test_hidden.txt'
        dir_list = fs.get_filelist(path, hidden=True)
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

    def test_simple_analyse(self):
        an = fs.simple_analyse(self.dir_list, self.base_dir)
        pd.testing.assert_frame_equal(an, self.data_frame)

    def test_simple_find(self):
        self.data_frame['Found'] = 0
        test_parser = argparse.Namespace(pattern='test', mode=1, ignore=False)
        expected_output = pd.DataFrame({'Full_Path': [self.dir_name], 'Path': [self.path], 'Lines': [4], 'Size': [17], 'Found': [2]})
        fs.simple_find(test_parser, self.data_frame)
        pd.testing.assert_frame_equal(self.data_frame, expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_full_find(self, mock_stdout):
        test_parser = argparse.Namespace(pattern='test', mode=0, ignore=False)
        fs.full_find(test_parser, self.data_frame)
        result = '\033[93m' + '\33[1m' + self.dir_name + '\033[0m'
        result = result + '\n' + '      ' + '\033[91m' + 'test' + '\033[0m' + '\n' + '      ' + '\033[91m' + 'TEST' + '\033[0m' + '\n'
        self.assertEqual(mock_stdout.getvalue(), result)

    def test_search_many_matches(self):
        pattern = 'password|test|123|dragon'
        line = 'password 64646 test gdgd 123 xxxx dragon ogferowg'
        result = fs.search(pattern, line)
        expected_output = b'\x1b[91mpassword\x1b[0m 64646 \x1b[91mtest\x1b[0m gdgd \x1b[91m123\x1b[0m xxxx \x1b[91mdragon\x1b[0m ogferowg'.decode('utf-8')
        self.assertEqual(result, expected_output)

    def test_search_return_mode(self):
        pattern = 'test'
        line = 'test test test'
        result = fs.search(pattern=pattern, line=line, return_mode=1)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0], 3)
        self.assertEqual(result[1], 1)

    def test_simple_find_list_length(self):
        self.data_frame['Found'] = 0
        self.data_frame['Matched'] = 0
        self.data_frame['%Matched'] = 0
        test_parser = argparse.Namespace(pattern='123', mode=1, ignore=False)
        expected_output = pd.DataFrame({'Full_Path': [self.dir_name], 'Path': [self.path], 'Lines': [4], 'Size': [17], 'Found': [2], 'Matched': 1, '%Matched': 0.25})
        fs.simple_find(test_parser, self.data_frame, 4)
        pd.testing.assert_frame_equal(self.data_frame, expected_output)