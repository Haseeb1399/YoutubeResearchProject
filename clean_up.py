'''
Code Author: Harris Ahmad

This script navigates through your main directory and removes any empty folders (if any)
to make it easy for you to keep track of what folders have actual content. 
'''

import os
import shutil

ROOT_DIR = 'E:/Summers_2022/research'  # specify your root working directory


def removeEmptyFolders(root_directory: str) -> None:
    '''
    This function deletes all unwanted directories
    '''
    all_directories = list(os.walk(root_directory))
    for path, _, _ in all_directories:
        if len(os.listdir(path)) == 0:  # Checking if the directory is empty or not
            shutil.rmtree(path)  # Delete the folder if it is empty


def removeEmptyFiles(root_directory: str) -> None:
    '''
    This function iterates through the directories
    and deletes any unwanted/ empty files.
    Caution: this only works for files and not directories
    or subdirectories.
    '''
    for path, _, files in os.walk(root_directory):
        for file in files:
            target = '{}/{}'.format(path, file)
            if os.path.isfile(target):
                size_target = os.path.getsize(target)
                if size_target == 0:
                    os.remove(target)


if __name__ == '__main__':
    removeEmptyFiles(ROOT_DIR)
    removeEmptyFolders(ROOT_DIR)
