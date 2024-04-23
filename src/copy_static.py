import os
import shutil


def copy_directory(src, dest):
    if not os.path.exists(src):
        raise ValueError("src does not exist")
    if os.path.isfile(dest) or os.path.isfile(src):
        raise ValueError("src and dest must be a directory")
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    
    os.mkdir(dest)
    
    for d in os.listdir(src):
        if os.path.isfile(os.path.join(src, d)):
            shutil.copy(os.path.join(src, d), dest)
        else:
            copy_directory(os.path.join(src, d), os.path.join(dest, d))