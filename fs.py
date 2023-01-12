import os
import argparse


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
    args = parser.parse_args()
    return args


def get_dirlist(directory: str):
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

    for path, currentDirectory, files in os.walk(path):
        for file in files:
            result = os.path.join(path, file)
            dir_list.append(result)

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
    file = open(path,'rb')
    output = []
    for line in file.readlines():
        result = ''
        for character in line:
            char = chr(character)
            if char.isprintable():
                result += char
        output.append(result)

    return output


def main():
    pass


if __name__ == '__main__':
    main()
