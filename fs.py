import os
import argparse
import re
import pandas as pd


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments

    --------
    Returns:
        argparse: Command line arguments
    """

    parser = argparse.ArgumentParser(
        description='Searches for a given string in all files in a directory and its subdirectories.'
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
        type=int,
        help='Descend only level directories deep'
    )

    parser.add_argument(
        '-n',
        '--hidden',
        action='store_true',
        help='Include hidden files and directories'
    )

    args = parser.parse_args()
    return args


def get_filelist(directory: str, hidden: bool = False, extensions: str = None, level: int = -1):
    """
    Get all filenames in given directory

    Parameters:
    ----------
    directory: str
        Path to the directory to search.

    hidden: bool
        Include hidden files in output

    extensions: str
        List of file extensions to exclude.

    level: int
        Descend only level directories deep


    --------
    Returns:
        list: All paths to files in a given directory and subdirectories recursively
    """

    path = os.path.abspath(directory)
    file_list = []
    extensions = extensions.split(',') if extensions is not None else []
    if os.path.isdir(path):
        for root, currentDirectory, files in os.walk(path):
            for m_file in files:
                result = os.path.join(root, m_file)
                path_level = get_path_level(path, result)
                if path_level <= level or level == -1:
                    file_list.append(result)
                    if is_hidden(result) and not hidden:
                        file_list.remove(result)
    else:
        file_list.append(path)

    files = []

    for extension in extensions:
        for path in file_list:
            if not path.endswith(extension) and path not in files:
                files.append(path)

    file_list = files if len(extensions) > 0 else file_list

    return file_list


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


def search(pattern: str, line: str, case_sensitive: bool = False) -> str:
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


def simple_analyse(dirlist: list, base_dir: str):
    """
    Returns basic information about file in pandas table format

    Parameters:
    ----------
    dirlist: list
        List of full paths of files to read

    base_dir: str
        A root of the path that is common to all

    --------
    Returns:
        pandas.DataFrame: Table with basic information of the file

    """
    data = []
    for path in dirlist:
        m_file = open(path, 'r')
        count = 0
        for _ in m_file:
            count += 1
        data.append([path[len(base_dir): len(path)], count, os.path.getsize(path)])
        m_file.close()

    df = pd.DataFrame(data, columns=["Path", "Lines", "Size"])

    return df


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

    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    parser = parse_args()

    dirlist = get_filelist(directory=parser.dir, hidden=parser.hidden, extensions=parser.extensions, level=int(parser.level))
    data = simple_analyse(dirlist, parser.dir)
    print(data)


if __name__ == '__main__':
    main()
