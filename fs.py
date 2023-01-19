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
        action='store_true',
        help='Ignore case distinctions in patterns and data'
    )

    parser.add_argument(
        '-x',
        '--extensions',
        help='File extension(s) to search for. Every extension is given after comma. eg. txt,php'
    )

    parser.add_argument(
        '-l',
        '--level',
        default=-1,
        help='Descend only level directories deep'
    )

    args = parser.parse_args()
    return args


def get_dirlist(directory: str, hidden: int = 0, extensions: str = None, level: int = -1):
    """
    Get all filenames in given directory

    Parameters:
    ----------
    directory: str
        Path to the directory to search.

    extensions: str
        List of file extensions to exclude.

    --------
    Returns:
        list: All paths to files in a given directory and subdirectories recursively
    """

    path = os.path.abspath(directory)
    dir_list = []
    extensions = extensions.split(',') if extensions is not None else []
    if os.path.isdir(path):
        for root, currentDirectory, files in os.walk(path):
            for file in files:
                result = os.path.join(root, file)
                path_level = get_path_level(path, result)
                if path_level <= level or level == -1:
                    dir_list.append(result)
                    if is_hidden(result) and hidden == 0:
                        dir_list.remove(result)
    else:
        dir_list.append(path)

    directory_list = []

    for extension in extensions:
        for path in dir_list:
            if not path.endswith(extension):
                directory_list.append(path)

    dir_list = directory_list if len(extensions) > 0 else dir_list

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

    case_sensitive : bool
        If True then ignore case distinctions in patterns and data

    --------
    Returns:
        str: If the pattern was found, return line with red-colored pattern.
    """

    regular = True if pattern[0] == '[' and pattern[-1] == ']' else False

    result = re.search(pattern, line, re.IGNORECASE) if case_sensitive else re.search(pattern, line)
    if result is not None:
        positions = re.finditer(pattern, line, re.IGNORECASE) if case_sensitive else re.finditer(pattern, line)
        positions = [m.start() for m in positions]
        pattern_length = 1 if regular else len(pattern)
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


def get_path_level(root_path: str, child_path: str):
    """
    Counts how many directories are between two paths with the same root.

    Parameters:
    ----------
    root_path: str
        Starting path

    child_path: str
        The final path between which the number of directories will be counted

    Returns:
        int: Number of paths between starting path and final path.
    """
    path = child_path[0 + len(root_path): -1]
    slashes = re.finditer('/', path)
    return len([slash.start() for slash in slashes])


def main():
    parser = parse_args()
    dirlist = get_dirlist(directory=parser.dir, extensions=parser.extensions, level=int(parser.level))
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
