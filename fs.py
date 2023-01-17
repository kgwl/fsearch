import os
import argparse
import re


def parse_args():
    """
    Parse command line arguments

    --------
    Returns:
        argparse: Command line arguments
    """

    parser = argparse.ArgumentParser(
        description='Search string in all files in directory'
    )
    parser.add_argument(
        '-d',
        '--dir',
        default='.',
        help='Path to the directory to search (default: %(default)s)'
    )

    parser.add_argument(
        'pattern',
        help='Pattern that is looked for'
    )

    parser.add_argument(
        '-i',
        '--ignore',
        action='store_true'
    )

    args = parser.parse_args()
    return args


def get_dirlist(directory: str, hidden: int = 0):
    """
    Get all filenames in given directory

    Parameters:
    ----------
    directory: str
        Path to the directory to search.

    --------
    Returns:
        list: All paths to files in a given directory and subdirectories recursively
    """

    path = os.path.abspath(directory)
    dir_list = []

    if os.path.isdir(path):
        for root, currentDirectory, files in os.walk(path):
            for file in files:
                result = os.path.join(root, file)
                dir_list.append(result)
                if is_hidden(result) and hidden == 0:
                    dir_list.remove(result)
    else:
        dir_list.append(path)

    return dir_list


def string_file(path: str):
    """
    Return all printable characters from file.

    Parameters:
    ----------
    path : str
        Path to the file.

    --------
    Returns:
        list: All printable characters in file. Every line is a single element of the list.
    """
    file = open(path, 'rb')
    output = []
    for line in file.readlines():
        result = ''
        for character in line:
            char = chr(character)
            if char.isprintable():
                result += char
        output.append(result)

    file.close()

    return output


def search(pattern: str, line: str, case_sensitive: bool = False):
    """
    Returns line that contains given pattern. By default, the search pattern is displayed in red

    Parameters:
    ----------
    pattern : str
        The pattern that is looked for

    line : str
        Searched text

    --------
    Returns:
        str: If the pattern was found, return line with red-colored pattern.
    """

    result = re.search(pattern, line, re.IGNORECASE) if case_sensitive else re.search(pattern, line)
    if result is not None:
        positions = re.finditer(pattern, line, re.IGNORECASE) if case_sensitive else re.finditer(pattern, line)
        positions = [m.start() for m in positions]
        pattern_length = len(pattern) if len(positions) == 1 else 1
        index = 0
        output = ''
        for position in positions:
            output += line[index: position] + '\033[91m' + line[position: position + pattern_length] + '\033[0m'
            index = position + pattern_length
        output += line[index:]
        return output


def is_hidden(file_path: str):
    """
    Checks if the given directory or file is hidden. Function searches if the given path contains files with prefix '.'

    Parameters:
    ----------
    file_path : str
        path to the file or directory

    --------
    Returns:
        bool: True if path contains prefix. (file is hidden)
    """

    return re.search('/\.', file_path) is not None


def main():
    parser = parse_args()
    dirlist = get_dirlist(parser.dir)
    for path in dirlist:
        file = string_file(path)
        output = []
        for line in file:
            result = search(parser.pattern, line, parser.ignore)
            if result is not None:
                output.append(result)

        if len(output) > 0:
            print('\033[93m' + '\33[1m' + path + '\033[0m')
        for line in output:
            print('     ', line)


if __name__ == '__main__':
    main()
