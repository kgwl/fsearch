import os
import argparse


def parse_args():
    """
    Parse command line arguments
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

    Parameters
    ----------
    directory : str
        Path to the directory to search.
    """

    path = os.path.abspath(directory)
    dir_list = []

    for path, currentDirectory, files in os.walk(path):
        for file in files:
            result = os.path.join(path, file)
            dir_list.append(result)

    return dir_list


def main():
    pass


if __name__ == '__main__':
    main()
