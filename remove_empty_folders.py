'''
Code Author: Harris Ahmad

This script runs navigates through your main directory and removes any empty folders (if any)
to make it easy for you to keep track of what folders have actual content. 
'''

import os
import shutil

ROOT_DIR = 'E:/Summers_2022/research'


all_directories = list(os.walk(ROOT_DIR))
for path, _, _ in all_directories:
    if len(os.listdir(path)) == 0:  # Checking if the directory is empty or not
        shutil.rmtree(path)  # Delete the folder if it is empty
