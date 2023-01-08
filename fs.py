import os
import time
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
    fs_dir_list_name = '/tmp/fslist' + str(time.time_ns()) + '.txt'
    dir_list = []
    command = 'du -a ' + path + '| grep -o "/.*" > ' + fs_dir_list_name
    os.system(command)
    file = open(fs_dir_list_name)
    for line in file.readlines():
        line = line.replace('\n', '')
        line = line.replace(' ', '\\ ')
        if not os.path.isdir(line):
            dir_list.append(line)
    file.close()
    os.remove(fs_dir_list_name)
    return dir_list


def main():
    pass


if __name__ == '__main__':
    main()
