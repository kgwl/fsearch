import os
import time


def get_dirlist(directory: str):
    path = os.path.abspath(directory)
    fs_dir_list_name = '/tmp/fsdirlist' + str(time.time_ns()) + '.txt'
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
